
// before running in ROOT do:
// gSystem->Load("LecroyData_C.so");
// incomplete... but shows C++ syle macro


void deltaT(TString fname="lecroy.root"){

  TFile *tf=new TFile(fname);

  int evtNum;
  ChannelData *chan[4];
  for (int i=0; i<4; i++) chan[i]=new ChannelData();
  
  TTree *t=(TTree*)tf->Get("lecroy");
  
  
  t->SetBranchAddress("eventnum",&evtNum);
  t->SetBranchAddress("chan1",&chan[0]);
  t->SetBranchAddress("chan2",&chan[1]);
  t->SetBranchAddress("chan3",&chan[2]);
  t->SetBranchAddress("chan4",&chan[3]);

  UInt_t dw = gClient->GetDisplayWidth();
  UInt_t dh = gClient->GetDisplayHeight();
  int wid=dw*0.8;
  int hig=wid*0.6;
  TCanvas *tc=new TCanvas("tc", "test", wid, hig);
  tc->Divide(3,2);

  int MAXOVERLAY=10;
  TMultiGraph *tmg1=new TMultiGraph("tmg1","SIPM1");
  TMultiGraph *tmg2=new TMultiGraph("tmg2","SIPM2");
  TMultiGraph *tmg3=new TMultiGraph("tmg3","MCP");
  
  for (int i=0; i<t->GetEntries(); i++){
    t->GetEntry(i);
    if (i<MAXOVERLAY) {
      tmg1->Add(chan[1]->GetGraph());
      tmg2->Add(chan[2]->GetGraph());
      tmg3->Add(chan[3]->GetGraph());

    }
  }
  
  tc->cd(1); tmg1->Draw("AL");
  tc->cd(2); tmg2->Draw("AL");
  tc->cd(3); tmg3->Draw("AL");

  TMultiGraph *tmg4=new TMultiGraph("tmg4","SIPM1, MCP");
  t->GetEntry(0);
  tmg4->Add(chan[1]->GetGraph());
  tmg4->Add(chan[3]->GetGraph());
  tc->cd(4); tmg4->Draw("AL");

  
}



