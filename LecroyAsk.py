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
description = 'C{0}:INSP? "WAVEDESC"'
simple = 'C1:INSP? "SIMPLE",BYTE'
trigger = "TRIG_SELECT?"
trigset = 'TRSE EDGE,SR,C2,HT,OFF'
trigLevel = 'C2:TRLV -0.1V'
#inst.write('C4:COUPLING D50')
#inst.write('C3:COUPLING D50')
#inst.write('C2:COUPLING D50')
#inst.write(trigLevel)
#inst.write(trigset)
#inst.write('C3:AUTO_SETUP')
#inst.write('C4:AUTO_SETUP')
# print inst.ask(trigger)
#print inst.ask('C2:TRIG_LEVEL?')
# trigTime = waveformBase.format(2, 'TRIGGER_TIME')
# horizInterval = waveformBase.format(2, 'HORIZ_INTERVAL')
# vertUnit = waveformBase.format(2, 'VERTUNIT')
# data_array = waveformBase.format(2, 'DATA_ARRAY_1')
# data_array_size = waveformBase.format(2, 'WAVE_ARRAY_COUNT')
# template = 'TEMPLATE?'

#tmpl =  inst.ask(template)
#f = open('LecroyTemplate.txt','w')
#f.writelines(tmpl)
#f.close()
#print inst.ask(simple)

#print inst.ask('TDIV?')
print inst.ask(description.format(1))
print inst.ask(description.format(2))
print inst.ask(description.format(3))
print inst.ask(description.format(4))
print inst.ask(simple.format(1))
inst.close()
