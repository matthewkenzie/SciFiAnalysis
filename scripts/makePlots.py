#!/usr/bin/env python

import ROOT as r

r.gROOT.ProcessLine('.x /Users/matt/Scratch/lhcb/lhcbStyle.C')

tf = r.TFile('TheOutFile_temp.root')

ndp_d_025 = tf.Get('g_d0.25')
ndp_d_100 = tf.Get('g_d1.00')

f_ndp_d_025 = r.TF1('f_d0.25','expo+expo(2)',0,200)
f_ndp_d_100 = r.TF1('f_d1.00','expo+expo(2)',0,200)

f_ndp_d_100.SetParameter(0, 3.64447e+00)
f_ndp_d_100.SetParameter(1,-1.35442e-02)
f_ndp_d_100.SetParameter(2, 3.91209e+00)
f_ndp_d_100.SetParameter(3, 6.47131e-05)

ndp_d_025.Fit(f_ndp_d_025)
ndp_d_100.Fit(f_ndp_d_100)

f_ndp_d_025.SetLineColor(r.kBlue)
f_ndp_d_025.SetLineWidth(2)
f_ndp_d_100.SetLineColor(r.kRed)
f_ndp_d_100.SetLineWidth(2)

canv = r.TCanvas()

leg = r.TLegend(0.7,0.62,0.94,0.8)
leg.SetFillColor(0)
leg.AddEntry(f_ndp_d_025,'diam=0.25mm','L')
leg.AddEntry(f_ndp_d_100,'diam=1.00mm','L')

mg = r.TMultiGraph()
mg.Add(ndp_d_025)
mg.Add(ndp_d_100)
mg.Draw("AEP")
canv.Update()
canv.Modified()
mg.GetYaxis().SetRangeUser(0,120)
mg.GetYaxis().SetTitle("mean number of detected photons")
mg.GetXaxis().SetTitle("Fibre length (cm)")
mg.GetXaxis().SetTitleOffset(0.8)
mg.GetYaxis().SetTitleOffset(0.8)
mg.GetYaxis().SetTitleSize(0.6*mg.GetYaxis().GetTitleSize())

leg.Draw("same")
f_ndp_d_025.Draw("same")
f_ndp_d_100.Draw("same")

val_025 = f_ndp_d_025.Eval(0.)
val_100 = f_ndp_d_100.Eval(0.)

pave = r.TLatex()
pave.SetNDC()
pave.SetTextSize(0.04)
text = 'diam 0.25: @0cm Np=%4.1f    diam 1.00: @0cm Np=%4.1f'%(val_025,val_100)
pave.DrawLatex(0.15,0.86,text)

canv.Update()
canv.Modified()
canv.Print("plots/fit.pdf")

en_dep_025 = tf.Get('edepos_d0.25_l10.0')
en_dep_100 = tf.Get('edepos_d1.00_l10.0')

en_dep_025.SetLineWidth(2)
en_dep_025.SetLineColor(r.kBlue)
en_dep_100.SetLineWidth(2)
en_dep_100.SetLineColor(r.kRed)

hcanv = r.TCanvas()
dummy = r.TH1F("d","",1,0,300)
dummy.GetYaxis().SetRangeUser(0,3500)
dummy.GetXaxis().SetTitle('Energy deposited (keV)')
dummy.GetYaxis().SetTitle('nEvents')
dummy.GetXaxis().SetTitleOffset(0.8)
dummy.GetYaxis().SetTitleOffset(0.8)
en_dep_025.GetXaxis().SetTitle('Energy deposited')
en_dep_025.GetYaxis().SetTitle('nEvents')
en_dep_025.GetXaxis().SetTitleOffset(0.8)
en_dep_025.GetYaxis().SetTitleOffset(0.8)
en_dep_100.GetXaxis().SetTitle('Energy deposited')
en_dep_100.GetYaxis().SetTitle('nEvents')
en_dep_100.GetXaxis().SetTitleOffset(0.8)
en_dep_100.GetYaxis().SetTitleOffset(0.8)
dummy.Draw()
en_dep_025.Draw("HISTsame")
en_dep_100.Draw("HISTsame")
leg.Draw("same")

# ignore evs at zero



pave.DrawLatex(0.25,0.86,'diam 0.25: <E>=%4.1f keV     diam 1.00: <E>=%4.1f keV'%(en_dep_025.GetMean(),en_dep_100.GetMean()))
pave.DrawLatex(0.25,0.80,'diam 0.25: Np (d=0) / E = %5.3f / keV'%(val_025/en_dep_025.GetMean()))
pave.DrawLatex(0.25,0.74,'diam 1.00: Np (d=0) / E = %5.3f / keV'%(val_100/en_dep_100.GetMean()))



hcanv.Update()
hcanv.Modified()
hcanv.Print("plots/edepos.pdf")

print 'd0.25:  N (d=0) / DeltaE = ', val_025/en_dep_025.GetMean()
print 'd1.00:  N (d=0) / DeltaE = ', val_100/en_dep_100.GetMean()


raw_input()
