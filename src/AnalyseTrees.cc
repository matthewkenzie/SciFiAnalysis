#include "../interface/AnalyseTrees.h"

using namespace std;

AnalyseTrees::AnalyseTrees():
  maxId(0),
  pho_yield(8.)
{}

AnalyseTrees::~AnalyseTrees(){

}

void AnalyseTrees::addFile(TString fileName){
  fileNames.push_back(fileName);
}

void AnalyseTrees::init(TString outFileName, TString outTreeName){

  outFile = new TFile(outFileName,"RECREATE");
  outTree = new TTree(outTreeName,"SciFi Sim Analysed");

  setOutputBranches();

  hists["nphos"] = new TH1F("nphos","",100,0,4000);
  hists["e_depos"] = new TH1F("e_depos","",100,0,500);

}

void AnalyseTrees::setOutputBranches(){

  outTree->Branch("myEvId",&myEvId);
  outTree->Branch("fileId",&fileId);
  outTree->Branch("runId",&runId);
  outTree->Branch("eventId",&eventId);
  outTree->Branch("nphos",&nphos);
  outTree->Branch("e_depos",&e_depos);

}

void AnalyseTrees::fill(){

  for (unsigned int ev=0; ev<eventInfo.size(); ev++){

    myEvId = int(ev);
    fileId = eventInfo[ev].fileId;
    runId = eventInfo[ev].runId;
    eventId = eventInfo[ev].eventId;
    nphos = eventInfo[ev].nphos;
    e_depos = double(eventInfo[ev].nphos)/pho_yield;

    if (eventId==0) {
      cout << myEvId << ": " << " f: " << fileId << " r: " << runId << " e: " << eventId << " nphos: " << nphos << endl;
    }

    outTree->Fill();

    hists["nphos"]->Fill(eventInfo[ev].nphos);
    hists["e_depos"]->Fill(eventInfo[ev].nphos/pho_yield);
  }

}

void AnalyseTrees::save(){

  outFile->cd();
  outTree->Write();
  for (map<TString,TH1F*>::iterator it=hists.begin(); it!=hists.end(); it++){
    it->second->Write();
  }
  outFile->Close();
  delete outFile;
}

void AnalyseTrees::setBranches(TTree *tree){
  tree->SetBranchAddress("runId",&runId);
  tree->SetBranchAddress("eventId",&eventId);
  tree->SetBranchAddress("creatorProcess",&creatorProcess);
}

void AnalyseTrees::run(){

  for (unsigned int f=0; f<fileNames.size(); f++){
    TFile *tf = TFile::Open(fileNames[f]);
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
        event.nphos = 0;

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
    tf->Close();
    delete tf;
  }
}

void AnalyseTrees::printEventInfo(){

  for (map<int,Event>::iterator evIt=eventInfo.begin(); evIt!=eventInfo.end(); evIt++){
    cout << evIt->first << ": " << " f: " << evIt->second.fileId << " r: " << evIt->second.runId << " e: " << evIt->second.eventId << " nphos: " << evIt->second.nphos << endl;
  }
}
