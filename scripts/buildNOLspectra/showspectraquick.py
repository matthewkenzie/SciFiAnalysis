#!/usr/bin/env python
import ROOT as r

gr = r.TGraph()

import sys

f = open(sys.argv[1])

p=0
for line in f.readlines():
  x = float(line.split()[0])
  y = float(line.split()[1])
  gr.SetPoint(p,x,y)
  p+=1

c = r.TCanvas()
gr.Draw("ALP")
c.Update()
c.Modified()
raw_input()

