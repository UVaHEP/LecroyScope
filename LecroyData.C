#include "LecroyData.h"
#include "TString.h"
#include "TMath.h"
#include <iostream>
#include <algorithm>
using std::cout;
using std::endl;

void ChannelData::SetTimeStamp(Int_t year, Int_t month, Int_t day,
			       Int_t hour, Int_t min, Int_t sec){
  tdatime.Set(year,month,day,hour,min,sec);
}

// default behavior is to set trigger time as t=0
// if calib==true, return calibrated volts, else raw ADC samples
// if sequential==true, time time is relative to 1st trigger in sequence
TGraph *ChannelData::GetGraph(Bool_t calib, Bool_t sequential) const {
  TGraph *tg=new TGraph();
  TString name=(TString::Format("Channel %d",chanID));
  tg->SetName(name);
  if (calib) name+=";t[sec];Volts";
  else name+=";t[sec];ADC";
  tg->SetTitle(name);

  Float_t offset=trgOffset;
  if (sequential) offset+=trgTime;
  for (unsigned i=0; i<v.size();i++){
    Float_t t=offset+tStep*i;
    Float_t yval=v[i];
    if (calib) yval=yval*vGain-vOffset;
    tg->SetPoint(i,t,yval);
  }
  return tg;
}


void ChannelData::SetSamples(char *dat, Int_t n) {
  v=vector<Char_t>((Char_t*)dat,dat+n);
  // estimate a "signal significance"
  vector<Char_t> v2 = v;
  std::sort(v2.begin(), v2.end());
  int median=v2[n/2];  // estimate of baseline
  //cout << chanID << " median " << median << endl;
  int up = (int) v2[n-1] - median;
  int dn = median - (int) v2[0];
  int max=TMath::Max(up,dn);   // max excursion from median
  int sum=0;
  for (int i=0; i<50; i++) {
    sum+=TMath::Abs((int)v[i]-median);
  }                        // estimate noise as mean excursion of points
  float noise=1.0*sum/25;  // around first samples in waveform.  This is ~OK,
  sigSig=max/noise-1;      // as long as there is no large pileup in that location
}



void ChannelData::Print() const{
  cout << "=== Channel " << chanID << " ===" << endl;
  cout << "Enabled " << chanOn << endl;
  if (! chanOn) return;
  cout << "N samples " << GetNpoints() << endl;
}



