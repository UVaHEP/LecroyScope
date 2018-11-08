import struct 

types = {
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


g = open('varlist.txt')
lines = g.readlines()
g.close()
split = map(lambda x: x.strip().split(','), lines)
cleaned =  map(lambda x: map(lambda y: y.strip(), x), split)


hdr = {} 
for i in cleaned:
    name,pos,typename = i
    pos = int(pos)
    hdr[name] = (pos, pos+types[typename], typename)


f = open('outputBin.dat','rb')

data = f.read()
f.close()

offset = 26
hdrdata = {}
end = 0 
for k in hdr.keys():
    name = k
    start,stop,typename = hdr[k]
    start = start+offset
    stop = stop+offset
    if stop > end:
        end = stop
    
    hdrdata[start] = (name, map(ord, data[start:stop]), typename)
#    print name,start,stop,map(ord, data[start:stop])


keys =  hdrdata.keys()
keys.sort()
parsedHdr = {} 
for k in keys:
    
    name,kdata,typename = hdrdata[k]
#    print name, map(hex, data), typename
    if typename == 'long':
        parsedHdr[name] = kdata[0]+(kdata[1]<<8)+(kdata[2]<<16)+(kdata[3]<<20)
        #print name, data[0]+(data[1]<<8)+(data[2]<<16)+(data[3]<<20)
    elif typename == 'float':
        parsedHdr[name] = struct.unpack('f', ''.join(map(chr, kdata)))[0]
        #print name, struct.unpack('f', ''.join(map(chr, kdata)))[0]
    elif typename == 'double':
        parsedHdr[name] = struct.unpack('d', ''.join(map(chr, kdata)))[0]
        #print name, struct.unpack('d', ''.join(map(chr, kdata)))[0]
    elif typename == 'string':
        parsedHdr[name] = ''.join(map(chr, kdata))
        #print name, ''.join(map(chr, kdata))
    elif typename == 'enum':
        parsedHdr[name] = kdata[0]+(kdata[1]<<8)
        #print name, kdata[0]+(kdata[1]<<8)
    elif typename == 'word':
        parsedHdr[name] = kdata[0]+(kdata[1]<<8)
        #print name, kdata[0]+(kdata[1]<<8)
    elif typename == 'time_stamp':
        parsedHdr[name] = struct.unpack('d', ''.join(map(chr, kdata)))[0]
        #print name, struct.unpack('d', ''.join(map(chr, kdata)))[0]
    elif typename == 'unit_definition':
        parsedHdr[name] = ''.join(map(chr, kdata))
        #print name, ''.join(map(chr, kdata))


print 'trigtime array', parsedHdr['TRIGTIME_ARRAY']
print 'ris time array',parsedHdr['RIS_TIME_ARRAY']
print 'resarray1', parsedHdr['RES_ARRAY1']
print 'usertxt', parsedHdr['USER_TEXT']
print 'seq count', parsedHdr['SUBARRAY_COUNT']
print 'seq subarray count', parsedHdr['NOM_SUBARRAY_COUNT']
print 'wave array count', parsedHdr['WAVE_ARRAY_COUNT']
print 'wavearray', parsedHdr['WAVE_ARRAY_1']
print 'wavearray2', parsedHdr['WAVE_ARRAY_2']
print 'res array2',parsedHdr['RES_ARRAY2']
print 'res array3',parsedHdr['RES_ARRAY3']
trigtime =  data[end:end+parsedHdr['TRIGTIME_ARRAY']]
if len(trigtime)/16 == parsedHdr['SUBARRAY_COUNT']:
    print 'Trig Time data array looks good.'

seqcount = parsedHdr['SUBARRAY_COUNT']
pos = 0
for i in range(0, seqcount):
    start = i*16
    stop = start+8
    print struct.unpack('d', trigtime[start:stop])
                        
print end
end = end+parsedHdr['TRIGTIME_ARRAY']
print end
print len(data)
waves = data[end:end+parsedHdr['WAVE_ARRAY_1']]
firstseq =  waves[0:(parsedHdr['WAVE_ARRAY_COUNT']/parsedHdr['SUBARRAY_COUNT'])]


out = open('test.dat','w')

for i in range(0, len(firstseq)):
#    print ord(firstseq[i])*parsedHdr['VERTICAL_GAIN']-parsedHdr['VERTICAL_OFFSET']
    out.write(str(ord(firstseq[i])*parsedHdr['VERTICAL_GAIN']-parsedHdr['VERTICAL_OFFSET']))
    out.write('\n')

out.close()
#combo = ''.join([firstseq[3], firstseq[2], firstseq[1], firstseq[0]])
#print struct.unpack('f', combo)
