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

seq = inst.ask("SEQUENCE?")
waveformSettings = inst.ask('WAVEFORM_SETUP?')
print 'Sequence: {0}, Waveform: {1}'.format(seq, waveformSettings)

#Enable Sequence Mode
inst.write('SEQ ON,500')
#inst.write('SEQ OFF')
seq = inst.ask("SEQUENCE?")
print 'Sequence: {0}, Waveform: {1}'.format(seq, waveformSettings)
inst.close()
