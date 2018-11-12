import argparse, sys

# keep ROOT TApplication from grabbing -h flag
from ROOT import PyConfig
PyConfig.IgnoreCommandLineOptions = True
from ROOT import *


def testreader(fname="lecroy.root",eventnum=0):

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

    t.GetEntry(eventnum)
    print "plotting event number",eventnum
    calibrate=False  # set to True to graph data in volts
    sequential=False # set to True to use sequentail times on x-axis
    for i in range(4):
        tc.cd(i+1)
        if chan[i].ChannelOn():
            chan[i].GetGraph(calibrate,sequential).Draw("ALP")

    tc.Update()
    return tc
    
if __name__ == '__main__':
    gSystem.Load("LecroyData_C.so")

    parser = argparse.ArgumentParser(description='Lecroy Data Test Plotter') 
    parser.add_argument('files', nargs='*', help="Give a filename or use default [lecroy.root]")
    parser.add_argument('-n','--eventnumber', type=int, default=0,
                        help="Event numebr to graph")
    args = parser.parse_args()

    if len(args.files)==0: fname="lecroy.root"
    else: fname=args.files[0]


    tc=testreader(fname,args.eventnumber)
    
    print 'Hit return to exit'
    sys.stdout.flush() 
    raw_input('')
    

