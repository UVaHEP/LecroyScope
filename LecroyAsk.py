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
description = 'C2:INSP? "WAVEDESC"'
simple = 'C2:INSP? "SIMPLE",BYTE'
trigTime = waveformBase.format(2, 'TRIGGER_TIME')
horizInterval = waveformBase.format(2, 'HORIZ_INTERVAL')
vertUnit = waveformBase.format(2, 'VERTUNIT')
data_array = waveformBase.format(2, 'DATA_ARRAY_1')
data_array_size = waveformBase.format(2, 'WAVE_ARRAY_COUNT')
template = 'TEMPLATE?'

tmpl =  inst.ask(template)
f = open('LecroyTemplate.txt','w')
f.writelines(tmpl)
f.close()
print inst.ask(simple)

print inst.ask('TDIV?')
print inst.ask_raw(description)
inst.close()
