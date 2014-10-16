#ifndef AnalyseTrees_h
#define AnalyseTrees_h

#include <iostream>
#include <vector>
#include <map>

#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"

struct Event {
  int fileId;
  int runId;
  int eventId;
  int nphos;
};

class AnalyseTrees {

  public:

    AnalyseTrees();
    ~AnalyseTrees();

    void addFile(TString fileName);
    void run();
    void printEventInfo();
    void init(TString outFileName, TString outTreeName);
    void fill();
    void save();

  private:

    std::vector<TString> fileNames;
    std::map<int,Event> eventInfo;
    void setBranches(TTree* tree);
    void setOutputBranches();
    TFile *outFile;
    TTree *outTree;
    std::map<TString,TH1F*> hists;

    int maxId;

    const double pho_yield;
    int runId;
    int eventId;
    int creatorProcess;

    int fileId;
    int myEvId;
    int nphos;
    double e_depos;

};

#endif
