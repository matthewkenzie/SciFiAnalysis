#/usr/bin/env python

import sys

import ROOT as r
r.gSystem.Load("lib/libAnalysis")
r.gROOT.SetBatch()

analyser = r.AnalyseTrees()

for f in sys.argv[1:]:
  analyser.addFile(f)
  print 'Added file', f

analyser.init("out.root","outtree")
analyser.run()
analyser.printEventInfo()
analyser.fill()
analyser.save()
