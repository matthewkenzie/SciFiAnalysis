#!/usr/bin/env python

import ROOT as r
import os

os.system('mkdir -p plots')

outf = r.TFile('TheOutFile.root','RECREATE')

diams = [0.25,1.00]
lengths = [10]
lengths= [10,20,30,50,100,200]

lcolors=[r.kBlack,r.kBlue,r.kRed,r.kGreen+1,r.kYellow-2,r.kMagenta]


def getHists(fname,ext,d=0):

  tf = r.TFile.Open(fname)
  tree = tf.Get('outtree')

  nphos_up = 1000
  e_depos_up = 150
  ndetphos_up = 100
  if d>0:
    nphos_up = 3000
    e_depos_up = 400
    ndetphos_up = 300

  nphos_h = r.TH1F('nphos_%s'%ext,'nphos',100,0,nphos_up)
  nphos_h.SetDirectory(0)
  e_depos_h = r.TH1F('edepos_%s'%ext,'e_depos',100,0,e_depos_up)
  e_depos_h.SetDirectory(0)
  ndetphos_h = r.TH1F('ndetphos_%s'%ext,'ndetphos',100,0,ndetphos_up)
  ndetphos_h.SetDirectory(0)

  for ev in range(tree.GetEntries()):
    tree.GetEntry(ev)
    if tree.nphos==0: continue
    nphos_h.Fill(tree.nphos)
    e_depos_h.Fill(tree.e_depos)
    ndetphos_h.Fill(tree.ndetphos)

  return (nphos_h, e_depos_h, ndetphos_h)

canv = r.TCanvas("c","c",1200,800)
canv.Divide(3,2)

gcanv = r.TCanvas("gc","gc",800,800)

all_h = []
all_g = []
all_g_en = []

canv.cd()
leg1 = r.TLegend(0.5,0.35,0.9,0.76)
leg1.SetFillColor(0)
leg2 = r.TLegend(0.5,0.35,0.9,0.76)
leg2.SetFillColor(0)
for d, diam in enumerate(diams):
  gr = r.TGraphErrors()
  gr.SetLineColor(lcolors[d+1])
  gr.SetMarkerColor(lcolors[d+1])
  gr.SetLineWidth(3)
  gr_en = r.TGraphErrors()
  gr_en.SetLineColor(lcolors[d+1])
  gr_en.SetMarkerColor(lcolors[d+1])
  gr_en.SetLineWidth(3)

  all_g.append(gr)
  all_g_en.append(gr_en)
  for l, length in enumerate(lengths):

    fname = 'files/fibre_widths/out_d%4.2f_l%4.1f.root'%(diam,length)

    nphos, energy, ndetphos = getHists(fname,'d%4.2f_l%4.1f'%(diam,length),d)
    all_h.append([nphos,energy,ndetphos])
    outf.cd()
    nphos.Write()
    energy.Write()
    ndetphos.Write()

    nphos.SetLineColor(lcolors[l])
    energy.SetLineColor(lcolors[l])
    ndetphos.SetLineColor(lcolors[l])

    if d==0:
      leg1.AddEntry(nphos,'Length = %4.1fcm'%(length/2.),'L')
      leg1.SetHeader('diam = 0.25mm')
    else:
      leg2.AddEntry(nphos,'Length = %4.1fcm'%(length/2.),'L')
      leg2.SetHeader('diam = 1.00mm')

    ndetphos.GetYaxis().SetRangeUser(0,4000)

    print 'nphos: (', diam,',',length,')', '--', nphos.GetMean()
    print 'energy: (', diam,',',length,')', '--', energy.GetMean()
    print 'ndetphos: (', diam,',',length,')', '--', ndetphos.GetMean()

    gr.SetPoint(l,length/2.,ndetphos.GetMean())
    gr.SetPointError(l,1.,ndetphos.GetMeanError())

    gr_en.SetPoint(l, length/2.,energy.GetMean())
    gr_en.SetPoint(l, 1., energy.GetMeanError())

    canv.cd((d*3)+1)
    if l==0:
      nphos.Draw("HIST")
    else:
      nphos.Draw("same")

    canv.cd((d*3)+2)
    if l==0:
      energy.Draw("HIST")
    else:
      energy.Draw("same")

    canv.cd((d*3)+3)
    if l==0:
      ndetphos.Draw("HIST")
    else:
      ndetphos.Draw("same")

    if d==0: leg1.Draw("same")
    else: leg2.Draw("same")
    canv.Update()
    canv.Modified()

canv.Update()
canv.Modified()
canv.Print("plots/hists.pdf")

all_f = []
mg = r.TMultiGraph()
for i, g in enumerate(all_g):
  f = r.TF1("f_d%4.2f"%diams[i],"expo(0)+expo(2)",0,120)
  f.SetLineWidth(2)
  f.SetLineColor(lcolors[i+1])
  g.SetName('g_d%4.2f'%diams[i])
  g.Fit(f,'N0')
  all_f.append(f)
  mg.Add(g)
  outf.cd()
  g.Write()
  f.Write()

for i, g in enumerate(all_g_en):
  g.SetName('g_en_d%4.2f'%diams[i])
  outf.cd()
  g.Write()

for i, f in enumerate(all_f):
  print 'diam: ', diams[i], ' -- at 0. = ', f.Eval(0.)

gcanv.cd()
mg.Draw("APE")
mg.GetYaxis().SetRangeUser(0,120)
mg.GetYaxis().SetTitle("mean number of detected photons")
mg.GetXaxis().SetTitle("Fibre length (cm)")

gcanv.Update()
gcanv.Modified()
gcanv.Print("plots/graphs.pdf")

outf.cd()
canv.Write()
gcanv.Write()
outf.Close()

raw_input()
