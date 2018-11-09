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
trigTime = waveformBase.format(2, 'TRIGGER_TIME')
horizInterval = waveformBase.format(2, 'HORIZ_INTERVAL')
vertUnit = waveformBase.format(2, 'VERTUNIT')
data_array = waveformBase.format(2, 'DATA_ARRAY_1')
data_array_size = waveformBase.format(2, 'WAVE_ARRAY_COUNT')
template = 'TEMPLATE?'

#print inst.ask(template)

data =  inst.ask(data_array)
count =  inst.ask(data_array_size).split(':')[2].strip()
interval = float(inst.ask(horizInterval).split(':')[2].split(' ')[1].strip())
vertical = inst.ask(vertUnit)
print vertical
#waveform = inst.ask_raw('WAVEFORM?')

inst.close()
print "I'm Done!"
count = int(count.split(' ')[0])
print count
#print data
f = open('output.dat','w')
for l in data:
    f.write(l)
f.close()
data = map( lambda x: x.strip(), data.split('"'))



points = map(float, data[1].split())
mvpoints = map(lambda x: x*1000, points)
arr = array.array('f', mvpoints)
timearr = array.array('f')
for i in range (0, count):
    timearr.append(i*interval*1e9)

print interval

f = open('output.csv','w')
for i in range(0,len(mvpoints)):
    f.write(str(mvpoints[i]))
    f.write(',')
    f.write(str(timearr[i]))
    f.write('\n')


#print waveform




