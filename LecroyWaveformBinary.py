import vxi11
import array 
import sys

host = 'hep-lecroy.phys.virginia.edu'

inst = None 
try: 
    inst = vxi11.Instrument(host)
except Exception as e:
    print e
    exit()

scope = inst.ask('*IDN?')
print 'Found {0}'.format(scope)

waveformBase = "C{0}:INSP? '{1}'"
data_array_size = waveformBase.format(2, 'WAVE_ARRAY_COUNT')
count =  inst.ask(data_array_size).split(':')[2].strip()
horizInterval = waveformBase.format(2, 'HORIZ_INTERVAL')
timeBase = waveformBase.format(2, 'TIMEBASE')
hinterval = inst.ask(horizInterval)
tBase = inst.ask(timeBase)
print "Count: {0}".format(count)
print "Horiz Interval: {0}".format(hinterval)
print "Timebase: {0}".format(tBase)
#Read out all channels
request = 'C{0}:WAVEFORM? "WAVEDESC"'
for i in range(1,5):
    data = inst.ask_raw(request.format(i))
    f = open('outputBinC{0}.dat'.format(i), 'w')
    f.write(data)
    f.close()
inst.close()


