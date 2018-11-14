#ifndef LECROYDATA_H
#define LECROYDATA_H

#include "TObject.h"
#include "TGraph.h"
#include "TDatime.h"
#include <vector>

using std::vector;

class ChannelData {
public:
  //ChannelData() : chanOn(false), chanID(-1) {;}
  ChannelData();
  ~ChannelData();

  // Simple Getters
  Bool_t ChannelOn() const {return chanOn;}
  Int_t ChannelID() const {return chanID;}
  Float_t Gain() const {return vGain;}
  Float_t Offset() const {return vOffset;}
  Float_t TimeStep() const {return tStep;} 
  Double_t TrgOffset() const {return trgOffset;}
  Double_t TrgTime() const {return trgTime;}
  TDatime TimeStamp() const {return tdatime;}
  Double_t TimeFine() const {return fracSec;}
  Bool_t SequenceMode() const {return seqMode;}
  Float_t SignalSig() const {return sigSig;} 
  Double_t T0() const {return t0;}
  Int_t GetNpoints() const {return v.size();}
  vector<Char_t> *GetSamples() {return &v;}
  vector<float> *GetTimes() {return &time;}
  
  // Simple Setters
  void SetChannelOn(Bool_t status=true) {chanOn=status;}
  void SetChannelID(Int_t i) {chanID=i;}
  void SetGain(Float_t g){vGain=g;}
  void SetOffset(Float_t o){vOffset=o;}
  void SetTimeStep(Float_t t) {tStep=t;}
  void SetTrgOffset(Double_t t) {trgOffset=t;}
  void SetTrgTime(Double_t t) {trgTime=t;}
  void SetSequenceMode(Bool_t s) {seqMode=s;}
  void SetT0(Double_t t) {t0=t;}
  void SetTimeStamp(Int_t year, Int_t month, Int_t day,
		    Int_t hour, Int_t min, Int_t sec);
  void SetTimeFine(Double_t sec){fracSec=sec;}

  //TGraph* GetGraph(Bool_t calib=false, Bool_t sequential=false) const ;
  TGraph* GetGraph(Bool_t calib=false, Bool_t sequential=false) ;
  //  void AddSample(Float_t s) {v.push_back(s);}
  void SetSamples(char *dat, Int_t n);
  void SetTimes(float *dat, Int_t n);
  Int_t GetNsamples() const {return v.size();}
  void ClearSamples() {v.clear();}
  void ClearTimes() {time.clear();}
  Float_t GetTimeUncert() const {return horizUncert;}
  void Print() const;

  // data types below match definions in binary data block
private:
  // header data
  Float_t   vGain;         // vertical gain
  Float_t   vOffset;       // vewrtical offset
  Double_t  tStep;         // sample time step
  Bool_t    seqMode;       // trigger preserve time sequence?
  Float_t   horizUncert;   // time measurement uncertainty
  TDatime   tdatime;       // timestamp for DAQ start
  Double_t  fracSec;       // fraction of second to add to tdatime
  Int_t     chanID;        // channel ID=[0..3]
  Bool_t    chanOn;        // True is channel is used
  
  // wave data
  Int_t nSamples;
  Double_t  trgTime;       // trigger time for sequence mode
  Double_t  trgOffset;     // DAQ start relative to trigger
  Double_t  t0;            // offset time from 1st trigger for sequence mode
  // volts[i] = v[i]*v_gain-v_off
  vector<Char_t> v;        // voltage samples as signed characters
  vector<float> time;         // time stored at t0 + iterator*tStep
  Float_t sigSig;          // estimate of signal significiance

  TGraph *tg;

  //ClassDef(ChannelData,1)      //Event Header
  ClassDef(ChannelData,2)      //Event Header
};



#ifdef __CINT__
#pragma link C++ class ChannelData+;
#endif

#ifdef __MAKECINT__
#pragma link C++ class vector<Float_t>+;
#endif

#endif
