import argparse, sys, os

# keep ROOT TApplication from grabbing -h flag
from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True
from ROOT import *


def hitCounter(fname="lecroy.root", eventnum=0):

    tf=TFile(fname)
    
    t=tf.Get("lecroy")

    chan=[]
    for i in range(4):
        chan.append(ChannelData())

    t.SetBranchAddress("chan1",AddressOf(chan[0]))
    t.SetBranchAddress("chan2",AddressOf(chan[1]))
    t.SetBranchAddress("chan3",AddressOf(chan[2]))
    t.SetBranchAddress("chan4",AddressOf(chan[3]))

    h=1200
    w=int(1.618*h)
    tc=TCanvas("tc","Test reader",w,h)
    tc.Divide(4,1)

    iEntry = 0
    print t.GetEntries()
    nSignalEvents = 0
    hadOneGoodEvent = False

    while iEntry < t.GetEntries():
              
        t.GetEntry(iEntry)
        calibrate=False  # set to True to graph data in volts
        sequential=False # set to True to use sequential times on x-axis

        # drawing for selected event if asked
        #if iEntry == eventnum:
        #    print "plotting event number",eventnum
        #    for i in range(4):
        #        tc.cd(i+1)
        #        if chan[i].ChannelOn():
        #            chan[i].GetGraph(calibrate,sequential).Draw("ALP")        
        #    tc.Update()

        # check every event for signals in SiPMs
        channelAmp = [0,0,0,0]
        for i in range(4):
            if chan[i].ChannelOn():
                if iEntry == 464:
                    print iEntry, 'channel# ', i
                gr = chan[i].GetGraph(calibrate,sequential)
                if iEntry == 464:
                    print "past GetGraph"
                maxVal = gr.GetHistogram().GetMaximum()
                if iEntry == 464:
                    print "past maxVal"
                minVal = gr.GetHistogram().GetMinimum()
                if iEntry == 464:
                    print "past minVal"
                channelAmp[i] = abs(maxVal - minVal) # store channel info for all channels
                del gr
                # print some stuff
                #if abs(maxVal - minVal)> 10:
                #    print iEntry, i, minVal, maxVal
        # count events passing some signal cuts
        if channelAmp[1] > 10 and channelAmp[2] > 10:
            nSignalEvents = nSignalEvents + 1
            #print "{0} is a good event!".format(iEntry)
            
            if hadOneGoodEvent == False:
                print "plotting first good entry in event (iEntry == ({0})".format(iEntry)
                if chan[i].ChannelOn():
                    for i in range(4):
                        tc.cd(i+1)
                        if chan[i].ChannelOn():
                            chan[i].GetGraph(calibrate,sequential).Draw("ALP")        
                    tc.Update()
                    hadOneGoodEvent = True
                print "done plotting"
        # go to next event
        iEntry = iEntry + 1

    print "Number of Good Signal events in file: {0}".format(nSignalEvents)

    del tf, t, chan

    return tc, nSignalEvents
    
if __name__ == '__main__':
    gSystem.Load("LecroyData_C.so")

    parser = argparse.ArgumentParser(description='Lecroy Data Test Plotter') 
    parser.add_argument('files', nargs='*', help="Give a filename, directory, or use default [lecroy.root]")
    parser.add_argument('-n','--eventnumber', type=int, default=0,
                        help="Event numebr to graph")
    args = parser.parse_args()

    if len(args.files)==0: fname="lecroy.root"
    else: fname=args.files[0]


    nGoodEvents = 0
    
    if not os.path.isdir(os.path.join(os.path.abspath("."), fname)): #input is single file
        tc, nGoodEvents = hitCounter(fname, args.eventnumber)
        print "Number of good events in single file: {0}".format(nGoodEvents)
    else: #input is directory
        dirObjects = os.listdir (fname) # get all files and folders names in the current directory
        rootFiles = []
        #print dirObjects
        for name in dirObjects: # loop through all the files and folders
            if not os.path.isdir(os.path.join(os.path.abspath("."), name)): # check whether the current object is a file
                if '.root' in name and name.split('.root')[1]=='':
                    print fname+'/'+name
                    tc, tempGoodEvents = hitCounter( fname+'/'+name, args.eventnumber)
                    print "Number of good events in {0}: {1}".format(name, tempGoodEvents)
                    nGoodEvents = nGoodEvents + tempGoodEvents
                    del tc
        print "Number of good events in directory {0}: {1}".format(fname, nGoodEvents)
        
    print 'Hit return to exit'
    sys.stdout.flush() 
    raw_input('')
    

