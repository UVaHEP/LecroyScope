import struct,sys
import argparse
from array import array
from math import modf
import glob 
import os.path 


# keep ROOT TApplication from grabbing -h flag
from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True
from ROOT import *

# basic header info 
HEADER_OFFSET=26  # 26 byte offset
HEADER_SIZE=372   # fixed header size bfore start of USER_TEXT
WAVE_SOURCE=344+HEADER_OFFSET 


scopeTypes = {
    'string':16,
    'byte':1,
    'word':2,
    'long':4,
    'float':4,
    'double':8,
    'enum':2,
    'time_stamp':16,
    'data':1,
    'unit_definition':48,
    'text':160
}

def processPoint(point, v_gain, v_off):
    #print '{0},{1},{2},{3}'.format(point, v_gain, v_off, point*v_gain-v_off)
    return point*v_gain-v_off

def processLong(lng):
    return lng[0]+(lng[1]<<8)+(lng[2]<<16)+(lng[3]<<20)

    
def processInteger(i):
    tot = 0
    for byte in range(0, len(i)):
        shift = ord(i[byte]) << (8*byte)
        tot += shift
    return tot

def processFloat(f):
    return struct.unpack('f', ''.join( f))[0]

def processDouble(d):
    return struct.unpack('d', ''.join( d))[0]

def processType(d, typename):
    if typename == 'long':
        return processInteger(d)
    elif typename == 'float':
        return processFloat(d)
    elif typename == 'double':
        return processDouble(d)
    elif typename == 'time_stamp':
        #print ord(d[8]),ord(d[9]),ord(d[10]),ord(d[11]),int(ord(d[12])+ord(d[13])*256)
        tmp=d[0:8]
        sec=processDouble(tmp)
        min=ord(d[8])
        hr=ord(d[9])
        day=ord(d[10])
        month=ord(d[11])
        year=int(ord(d[12])+ord(d[13])*256)
        #print "data size", len(d),len(tmp)
        return sec,min,hr,day,month,year
    elif typename == 'string':
        return ''.join(d)
    elif typename == 'enum' or typename == 'word':
        return processInteger(d)
    elif typename == 'unit_definition':
        return ''.join(d)
    else:
        return None
    

def getHeaderTemplate(varfile):
    g = open(varfile)
    lines = g.readlines()
    g.close()
    split = map(lambda x: x.strip().split(','), lines)
    cleaned =  map(lambda x: map(lambda y: y.strip(), x), split)    
    hdrtpl = {} 
    for i in cleaned:
        name,pos,typename = i
        pos = int(pos)
        hdrtpl[name] = (pos, pos+scopeTypes[typename], typename, scopeTypes[typename])
    return hdrtpl; 


def printHeader(header,brief=False):
    print "data summary:"
    print 'header size',header['END']-header['OFFSET']
    print 'trg data start',header['TRIGGER_START']
    print 'voltage data start',header['WAVE_START']
    print '# of waves {0}'.format(header['NWAVES'])
    print '# samples/wave {0}'.format(header['SEQ_LEN'])
    if not brief:
        print '========= partial dump of header data ========'
        print 'COMM_TYPE {0}'.format(header['COMM_TYPE'][2])
        print 'COMM_ORDER {0}'.format(header['COMM_ORDER'][2])
        print 'usertxt', header['USER_TEXT'][2]
        print 'trigtime array', header['TRIGTIME_ARRAY'][2]  # trg start/offset for seq mode
        print 'ris time array',header['RIS_TIME_ARRAY'][2]
        print 'resarray1', header['RES_ARRAY1'][2]
        print 'wavearray', header['WAVE_ARRAY_1'][2]
        print 'wavearray2', header['WAVE_ARRAY_2'][2]
        print 'res array2',header['RES_ARRAY2'][2]
        print 'res array3',header['RES_ARRAY3'][2]
        print 'wave array count', header['WAVE_ARRAY_COUNT'][2]
        print 'points', header['PNTS_PER_SCREEN'][2]
        print 'first valid pt {0}'.format(header['FIRST_VALID_PNT'][2])
        print 'last valid pt {0}'.format(header['LAST_VALID_PNT'][2])
        print 'seq count', header['SUBARRAY_COUNT'][2]
        print 'Vertical Gain',header['VERTICAL_GAIN'][2]
        print 'Vertical Offset',header['VERTICAL_OFFSET'][2]
        print 'seq subarray count', header['NOM_SUBARRAY_COUNT'][2]
        print 'vert unit',header['VERT_UNIT'][2]
        print 'horiz unit',header['HORIZ_UNIT'][2]     # trigger offset (non seq mode)
        print 'horiz uncertainty',header['HORIZ_UNCERTAINTY'][2] 
        print 'DAQ start', header['TRIGGER_TIME'][2]   # time stamp in Y:M:D format
        print 'Channel ID', header['WAVE_SOURCE'][2]

   
     

        
def getHeader(data):
	# Varlist.txt contains a list of the WAVEDESC header from
	# the Template provided by our Lecroy scope.
	# Below generates a dictionary with the binary layout
	# of the header and the types in the header 
	hdrtpl = getHeaderTemplate('varlist.txt')
        
        # Offset determined from template, 26 bytes before you get to the wave header
	offset = HEADER_OFFSET
	hdrdata = {}
	end = 0
	header = {}
	for k in hdrtpl.keys():
	    name = k
	    start,stop,typename,typesize = hdrtpl[k]
	    start = start+offset
	    stop = stop+offset
	    if stop > end:
		end = stop
	    unprocessed = data[start:stop]
	    header[name] = (start, stop, processType(unprocessed, typename))
            #print name,header[name]

        # derived quantities
        header['OFFSET']=offset
        header['END']=end # position of end of header data
        header['TRIGGER_START']=end+header['USER_TEXT'][2]
        header['TRIGGER_SIZE']=header['TRIGTIME_ARRAY'][2]
        header['WAVE_START']=header["TRIGGER_START"]+header['TRIGTIME_ARRAY'][2]+header['RIS_TIME_ARRAY'][2]
        seqLen=header['WAVE_ARRAY_COUNT'][2]/header['SUBARRAY_COUNT'][2]

        # redundant, but for convenience
        header['SEQ_LEN']=seqLen
        header['NWAVES']=header['SUBARRAY_COUNT'][2]
        if header['TRIGTIME_ARRAY'][2] != 0: header['SEQ_MODE']=True
        else: header['SEQ_MODE']=False
        header['ChanID']=header['WAVE_SOURCE'][2]
        #header['NSAMPLES']=
        return header

# return list of trigger times in tuple (time from 1st trigger, offset from current trigger)
def getTrigTime(seqcount,trigtime):
    trigTime = []
    pos = 0
    for i in range(0, seqcount):
	start = i*16
	stop = start+8
	trigTime.append((struct.unpack('d', trigtime[start:stop])[0], struct.unpack('d', trigtime[stop:stop+8])[0]))
        #print trigTime[-1]
    return trigTime



def dumpWave(fname,time,volts):
    f = open(fname,'w')
    for pt in range(0,len(volts)):
        f.write(str(time[pt]))
	f.write(',')
        f.write(str(volts[pt]))
        f.write('\n')
    f.close()


    
def fillHeader(chan,chdat):
    n=chdat.header['ChanID']
    chan[n].SetChannelOn()
    chan[n].SetChannelID(n)
    chan[n].SetGain(ch.header['VERTICAL_GAIN'][2])
    chan[n].SetOffset(ch.header['VERTICAL_OFFSET'][2])
    chan[n].SetTimeStep(ch.header['HORIZ_INTERVAL'][2])
    chan[n].SetTrgOffset(ch.header['HORIZ_OFFSET'][2])
    chan[n].SetSequenceMode(ch.header['SEQ_MODE'])
    td=ch.header['TRIGGER_TIME'][2]
    sec=modf(td[0])
    chan[n].SetTimeStamp(td[5],td[4],td[3],td[2],td[1],int(sec[1]))
    chan[n].SetTimeFine(sec[0])



# simple function to read a channel ID from a file
def ReadChanID(fname):
    f = open(fname,'rb')
    f.seek(WAVE_SOURCE)
    d=f.read(2)
    chanID=processInteger(d)
    f.close()
    return chanID

# for ~convenient access data files
class ChanDat:
    """Lecroy wave form file"""
    def __init__(self,fname):
        self.f=open(fname,"rb")
        self.header=getHeader(self.f.read(HEADER_SIZE)) # fetch and decode header block
        self.trgTime=[]
        if self.header['SEQ_MODE']:
            self.f.seek(self.header['TRIGGER_START'])
            self.trgTime=getTrigTime( self.header['NWAVES'] , self.f.read(self.header["TRIGGER_SIZE"]) )
    def GetSamples(self,n):
        waveStart=self.header['WAVE_START']
        nsamples=self.header['SEQ_LEN']
        self.f.seek(waveStart+n*nsamples)
        raw=array('c')  # array of signed characters
        raw.fromfile(self.f,nsamples)
        return raw
        self.f.seek(waveStart+n*nsamples)
        seq=self.f.read(nsamples)
        v_gain = self.header['VERTICAL_GAIN'][2]
        v_off = self.header['VERTICAL_OFFSET'][2]
        volts = self.header['SEQ_LEN']*[None]
        for pt in range(nsamples):
            vVal = ord(seq[pt])
	    if vVal > 127: vVal -= 256
            volts[pt]=processPoint(vVal, v_gain, v_off)
        return volts,raw
            
    def PrintHeader(self):
        printHeader(self.header)


# open 1..4 data files in parallel and fill TTree with scope channel data
# -n limits number of events to be read
# -z applies zero suppression: requires hits in chan 1 & (2||3 ) & 4
#    ZSP thresholds are defined below and calculated in LecroyData::SetSamples
#    This is an ad hoc definition.
# -o optionial output file name

if __name__ == '__main__':
    debug=False

    # setup
    gROOT.ProcessLine(".! make")
    gSystem.Load("LecroyData_C.so")
    
    parser = argparse.ArgumentParser(description='Lecroy Data Processor') 
    parser.add_argument('files', nargs='*', help="Give file paths or a [filename].list to \
    specify channel data files.")
    parser.add_argument('-n','--nmax', type=int, default=9999,
                        help="Maximum number of events to process")
    parser.add_argument('-z','--useZSP', default=None, action="store_true",
                        help="use zero suppression to require signal")
    parser.add_argument('-d','--directory', default=None, 
                        help="directory to process")
    parser.add_argument('-o','--output', type=str, nargs='?', default='lecroy.root',
                        help="Output root file")
    
    # zero supression thresholds in term of sigSig variable of ChannelData
    zspvals=[20]*4
    
    args = parser.parse_args()



    if args.directory != None:
        flist = glob.glob(os.path.join(args.directory,'*.dat'))
        comb = map(lambda x: os.path.join(args.directory, x), flist)
        print comb
        args.files = comb
    if len(args.files)==0:
        print "No files to process"
        sys.exit(1)
    if len(args.files)>4:
        print "Too many files, only 4 channels can be defined"
        sys.exit(1)

    # fetch the channel data
    chandat=[None]*4        # data file handlers
    
    for fn in args.files:
        chanID=ReadChanID(fn)
        print "processing",fn,"found Channel ID",chanID
        chandat[chanID]=ChanDat(fn)
        print "read", chandat[chanID].header['NWAVES'],"events"
        if debug: chandat[chanID].PrintHeader()
        if args.useZSP: print "applying zero suppression"


    # check that number of triggers is the same in each channel dat file
    ntrig=None
    for ch in chandat:
        if not ch: continue
        if not ntrig: ntrig=ch.header['NWAVES']
        else: assert ntrig == ch.header['NWAVES'], "Data error: trigger counts do not match"

        
    tf=TFile(args.output,"RECREATE")
    t=TTree("lecroy","Waveform data")

    chan=[]
    for i in range(4):
        chan.append(ChannelData())

    evtNum = array('i',[0])
    t.Branch('eventnum', evtNum, 'evtNum/I')
        
    t.Branch("chan1", "ChannelData", AddressOf(chan[0]))
    t.Branch("chan2", "ChannelData", AddressOf(chan[1]))
    t.Branch("chan3", "ChannelData", AddressOf(chan[2]))
    t.Branch("chan4", "ChannelData", AddressOf(chan[3]))

    t.SetBranchAddress("chan1",AddressOf(chan[0]))
    t.SetBranchAddress("chan2",AddressOf(chan[1]))
    t.SetBranchAddress("chan3",AddressOf(chan[2]))
    t.SetBranchAddress("chan4",AddressOf(chan[3]))

    for chdat in chandat:
        if chdat: fillHeader(chan,chdat)    
    
    fname = 'seq-ch{0}_{1}.dat'              # for debug
    for i in range(min(ntrig,args.nmax)):    # loop over waves
        for chdat in chandat:                # loop over available channel data
            if not chdat: continue
            n=chdat.header['ChanID']         # fill channel objects for tree
            chan[n].ClearSamples()
            raw=chdat.GetSamples(i)
            
            if debug:
                #time=ch.GetSampleTimes(i)  # add later
                time=[0]*len(raw)  
                dumpWave( fname.format(chdat.header['ChanID'],i) ,time, raw)

            if chan[n].SequenceMode():
                chan[n].SetTrgTime(chdat.trgTime[i][0])
                chan[n].SetTrgOffset(chdat.trgTime[i][1])

            chan[n].SetSamples(raw,len(raw))

        passEvent=True
        if args.useZSP:
            passTrig=chan[0].SignalSig()>zspvals[0]
            passSipm=chan[1].SignalSig()>zspvals[1] or chan[2].SignalSig()>zspvals[2]
            passMcp=chan[3].SignalSig()>zspvals[3]
            passEvent=passTrig and passSipm and passMcp
        if passEvent:
            evtNum[0]=i
            t.Fill()


    print "processed",i+1,"waves",t.GetEntries(),"saved"
    tf.Write()
    tf.Close()
 
