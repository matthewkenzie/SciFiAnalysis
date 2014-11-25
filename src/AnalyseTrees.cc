#include "../interface/AnalyseTrees.h"

using namespace std;

AnalyseTrees::AnalyseTrees():
  maxId(0),
  pho_yield(8.)
{}

AnalyseTrees::~AnalyseTrees(){

}

void AnalyseTrees::addFile(TString fileName, double f_diam, double f_length){

  File file;
  file.fileName = fileName;
  file.fibre_diam = f_diam;
  file.fibre_length = f_length;
  files.push_back(file);
}

void AnalyseTrees::init(TString outFileName, TString outTreeName){

  outFile = new TFile(outFileName,"RECREATE");
  outTree = new TTree(outTreeName,"SciFi Sim Analysed");

  setOutputBranches();

}

void AnalyseTrees::setOutputBranches(){

  outTree->Branch("myEvId",&myEvId);
  outTree->Branch("fileId",&fileId);
  outTree->Branch("runId",&runId);
  outTree->Branch("eventId",&eventId);
  outTree->Branch("fibre_diam",&fibre_diam);
  outTree->Branch("fibre_length",&fibre_length);
  outTree->Branch("nphos",&nphos);
  outTree->Branch("e_depos",&e_depos);
  outTree->Branch("ndetphos",&ndetphos);

}

void AnalyseTrees::fill(){

  for (unsigned int ev=0; ev<eventInfo.size(); ev++){

    myEvId = int(ev);
    fileId = eventInfo[ev].fileId;
    runId = eventInfo[ev].runId;
    eventId = eventInfo[ev].eventId;
    nphos = eventInfo[ev].nphos;
    ndetphos = eventInfo[ev].ndetphos;
    fibre_diam = eventInfo[ev].fibre_diam;
    fibre_length = eventInfo[ev].fibre_length;
    e_depos = double(eventInfo[ev].nphos)/pho_yield;

    //if (eventId==0) {
      //cout << myEvId << ": " << " f: " << fileId << " r: " << runId << " e: " << eventId << " nphos: " << nphos << endl;
    //}

    outTree->Fill();
  }

}

void AnalyseTrees::save(){

  outFile->cd();
  outTree->Write();
  outFile->Close();
  delete outFile;
}

void AnalyseTrees::setBranches(TTree *tree){
  tree->SetBranchAddress("runId",&runId);
  tree->SetBranchAddress("eventId",&eventId);
  tree->SetBranchAddress("creatorProcess",&creatorProcess);
}

void AnalyseTrees::run(){

  for (unsigned int f=0; f<files.size(); f++){
    TFile *tf = TFile::Open(files[f].fileName);
    TTree *tree = (TTree*)tf->Get("ProducedPhotons");
    cout << "Opened file: " << tf->GetName() << endl;

    setBranches(tree);

    int evCache = int(eventInfo.size());

    int eventsPerRun = int(tree->GetMaximum("eventId"))+1;
    int nRuns = int(tree->GetMaximum("runId"))+1;

    // expect nRuns*eventsPerRun evs per file so can initliase the counter with these
    int expectedNewEvents = eventsPerRun*nRuns;
    cout << "Initialised counters for f: " << f << " with " << expectedNewEvents << " new events" << endl;

    for (int r=0; r<nRuns; r++){
      for (int e=0; e<eventsPerRun; e++){
        Event event;
        event.fileId = f;
        event.runId = r;
        event.eventId = e;
        event.fibre_diam = files[f].fibre_diam;
        event.fibre_length = files[f].fibre_length;
        event.nphos = 0;
        event.ndetphos = 0;

        myEvId = evCache + r*(eventsPerRun) + e;

        eventInfo[myEvId] = event;
      }
    }

    for (int jentry=0; jentry<tree->GetEntries(); jentry++){
      tree->GetEntry(jentry);

      if (creatorProcess != 1) continue;

      myEvId = evCache + runId*(eventsPerRun) + eventId;

      if (jentry%25000==0) {
        cout << "Entry " << jentry << " / " << tree->GetEntriesFast() << endl;
      }

      eventInfo[myEvId].nphos += 1;

    }
    delete tree;

    TTree *detTree = (TTree*)tf->Get("DetectedPhotons");
    setBranches(detTree);
    for (int jentry=0; jentry<detTree->GetEntries(); jentry++){
      detTree->GetEntry(jentry);

      myEvId = evCache + runId*(eventsPerRun) + eventId;

      if (jentry%25000==0) {
        cout << "Entry " << jentry << " / " << detTree->GetEntriesFast() << endl;
      }

      eventInfo[myEvId].ndetphos += 1;
    }
    delete detTree;

    tf->Close();
    delete tf;
  }
}

void AnalyseTrees::printEventInfo(){

  for (map<int,Event>::iterator evIt=eventInfo.begin(); evIt!=eventInfo.end(); evIt++){
    cout << evIt->first << ": " << " f: " << evIt->second.fileId << " r: " << evIt->second.runId << " e: " << evIt->second.eventId << " nphos: " << evIt->second.nphos << endl;
  }
}
