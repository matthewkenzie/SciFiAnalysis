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
  int ndetphos;
  double fibre_diam;
  double fibre_length;
};

struct File {
  TString fileName;
  double fibre_diam;
  double fibre_length;
};

class AnalyseTrees {

  public:

    AnalyseTrees();
    ~AnalyseTrees();

    void addFile(TString fileName, double f_diam, double f_length);
    void run();
    void printEventInfo();
    void init(TString outFileName, TString outTreeName);
    void fill();
    void save();

  private:

    std::vector<File> files;
    std::map<int,Event> eventInfo;
    void setBranches(TTree* tree);
    void setOutputBranches();
    TFile *outFile;
    TTree *outTree;

    int maxId;

    const double pho_yield;
    int runId;
    int eventId;
    int creatorProcess;

    int fileId;
    int myEvId;
    int nphos;
    int ndetphos;
    double e_depos;
    double fibre_diam;
    double fibre_length;

};

#endif
