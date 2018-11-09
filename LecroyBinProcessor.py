import struct 



scopeTypes = {
    'string':16,
    'byte':1,
    'word':2,
    'long':4,
    'float':4,
    'double':8,
    'enum':2,
    'time_stamp':8,
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
    elif typename == 'double' or typename == 'time_stamp':
        return processDouble(d)
    elif typename == 'string':
        return ''.join(d)
    elif typename == 'enum' or typename == 'word':
        return processInteger(d)
    elif typename == 'unit_definition':
        return ''.join(d)
    else:
        return None
    



def generateHeader(varfile):
    g = open(varfile)
    lines = g.readlines()
    g.close()
    split = map(lambda x: x.strip().split(','), lines)
    cleaned =  map(lambda x: map(lambda y: y.strip(), x), split)
    
    hdr = {} 
    for i in cleaned:
        name,pos,typename = i
        pos = int(pos)
        hdr[name] = (pos, pos+scopeTypes[typename], typename, scopeTypes[typename])

    return hdr; 
    

# Varlist.txt contains a list of the WAVEDESC header from
# the Template provided by our Lecroy scope.
# Below generates a dictionary with the binary layout
# of the header and the types in the header 

hdr = generateHeader('varlist.txt')



f = open('outputBinC4.dat','rb')
data = f.read()
f.close()

# Offset determined from template, 26 bytes before you get to the wave header

offset = 26
hdrdata = {}
end = 0
header = {}
for k in hdr.keys():
    name = k
    start,stop,typename,typesize = hdr[k]
    start = start+offset
    stop = stop+offset
    if stop > end:
        end = stop
    unprocessed = data[start:stop]
    header[name] = (start, stop, processType(unprocessed, typename))
print 'first valid pt {0}'.format(header['FIRST_VALID_PNT'][2])
print 'last valid pt {0}'.format(header['LAST_VALID_PNT'][2])
print 'COMM_TYPE {0}'.format(header['COMM_TYPE'][2])
print 'COMM_ORDER {0}'.format(header['COMM_ORDER'][2])
print 'trigtime', header['TRIGGER_TIME'][2]
print 'trigtime array', header['TRIGTIME_ARRAY'][2]
print 'ris time array',header['RIS_TIME_ARRAY'][2]
print 'resarray1', header['RES_ARRAY1'][2]
print 'usertxt', header['USER_TEXT'][2]
print 'seq count', header['SUBARRAY_COUNT'][2]
print 'seq subarray count', header['NOM_SUBARRAY_COUNT'][2]
print 'wave array count', header['WAVE_ARRAY_COUNT'][2]
print 'wavearray', header['WAVE_ARRAY_1'][2]
print 'wavearray2', header['WAVE_ARRAY_2'][2]
print 'res array2',header['RES_ARRAY2'][2]
print 'res array3',header['RES_ARRAY3'][2]


trigTime = [] 
if header['TRIGTIME_ARRAY'][2] != 0:
    print 'Trig Time!'
    trigtime =  data[end:end+header['TRIGTIME_ARRAY'][2]]
    if len(trigtime)/16 == header['SUBARRAY_COUNT'][2]:
        print 'Trig Time data array looks good.'

    seqcount = header['SUBARRAY_COUNT'][2]
    pos = 0
    for i in range(0, seqcount):
        start = i*16
        stop = start+8
        trigTime.append((struct.unpack('d', trigtime[start:stop])[0], struct.unpack('d', trigtime[stop:stop+8])[0]))
                        
end = end+header['TRIGTIME_ARRAY'][2]
print 'end: {0}'.format(end)
print 'wave: {0}'.format(end+header['WAVE_ARRAY_1'][2])
waves = data[end:end+header['WAVE_ARRAY_1'][2]]
print end, end+header['WAVE_ARRAY_1'][2]


horinterval = header['HORIZ_INTERVAL'][2]
horoffset = header['HORIZ_OFFSET'][2]

seqLen = header['WAVE_ARRAY_COUNT'][2]/header['SUBARRAY_COUNT'][2]
print len(waves) , header['WAVE_ARRAY_1'][2]
out = open('test.dat','w')
fname = 'seq-{0}.dat'
for i in range(0, len(waves)/seqLen):
    start = i*seqLen
    stop = start+seqLen
    seq = waves[start:stop]
    v_gain = header['VERTICAL_GAIN'][2]
    v_off = header['VERTICAL_OFFSET'][2]
    f = open(fname.format(i),'w')
    for pt in range(0,len(seq)):
        f.write(str(horinterval*pt+trigTime[i][1]))
        f.write(',')
        f.write( str(processPoint(ord(seq[pt]), v_gain, v_off)))
        f.write('\n')

        
        out.write(str(horinterval*pt+trigTime[i][1]))
        out.write(',')
        out.write( str(processPoint(ord(seq[pt]), v_gain, v_off)))
        out.write('\n')
    f.close()
    out.write('\n\n------------\n\n')
out.close()
