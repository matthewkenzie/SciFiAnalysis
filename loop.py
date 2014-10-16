#!/usr/bin/env

import sys
import ROOT as r

photonsTree= r.TChain('ProducedPhotons')

for f in sys.argv[1:]:
  photonsTree.AddFile(f)

pho_yield=8.

events = {}

for ev in range(photonsTree.GetEntries()):
	photonsTree.GetEntry(ev)

	if photonsTree.creatorProcess != 1: continue

	if photonsTree.eventId not in events.keys():
		events[photonsTree.eventId] = {}
		events[photonsTree.eventId]['counter'] = 0

	events[photonsTree.eventId]['counter'] += 1

keys = events.keys()
keys.sort()

nphoH = r.TH1F('nphoH','',100,0,1600)
enH = r.TH1F('en_depos','',100,0,200)
r.gStyle.SetOptStat(11111111)

for ev in keys:
	en_depos = float(events[ev]['counter'])/pho_yield
	enH.Fill(en_depos)
	nphoH.Fill(events[ev]['counter'])

canv = r.TCanvas("c","c",800,1200)
canv.Divide(1,2)
canv.cd(1)
enH.Draw("HIST")
canv.cd(2)
nphoH.Draw("HIST")
canv.Update()
canv.Modified()
raw_input()

