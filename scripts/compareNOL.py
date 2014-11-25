#!/usr/bin/env python

import ROOT as r
r.gROOT.ProcessLine('.x /Users/matt/Scratch/lhcb/lhcbStyle.C')
r.gROOT.SetBatch()

colors = [r.kBlue, r.kRed, r.kGreen+1, r.kMagenta+2]

def compHist(trees, names, titles, varname, xtitle, ytitle,nbins,xmin, xmax, nameext="", cut=""):

  canv = r.TCanvas()
  canv.SetBottomMargin(0.2)
  canv.SetLeftMargin(0.2)

  leg = r.TLegend(0.6,0.6,0.89,0.89)
  leg.SetFillColor(0)

  hists = []

  maxy=0.
  for t, tree in enumerate(trees):
    hists.append(r.TH1F('h_%s_%s'%(names[t],varname),'',nbins,xmin,xmax))
    tree.Draw('%s>>%s'%(varname,hists[t].GetName()),cut)
    hists[t].SetLineWidth(2)
    hists[t].SetLineColor(colors[t])
    leg.AddEntry(hists[t],titles[t],"L")
    maxy = r.TMath.Max(maxy,hists[t].GetMaximum())

  dummy = r.TH1F('d','',1,xmin,xmax)
  dummy.GetXaxis().SetTitle(xtitle)
  dummy.GetXaxis().SetTitleOffset(0.9)
  dummy.GetYaxis().SetTitle(ytitle)
  dummy.GetYaxis().SetTitleOffset(0.9)
  dummy.GetYaxis().SetRangeUser(0,maxy*1.2)

  dummy.Draw()
  for hist in hists:
    hist.Draw("same")
  leg.Draw("same")

  canv.Update()
  canv.Modified()

  canv.Print("plots/%s%s.pdf"%(varname,nameext))
  canv.Print("plots/%s%s.png"%(varname,nameext))

  for hist in hists:
    r.gDirectory.Delete(hist.GetName())
    del hist

  del dummy
  del leg
  del canv

tf_Kurray       = r.TFile('files/NOL_NewAdditions/Kurray.root')
tf_NOL3         = r.TFile('files/NOL_NewAdditions/NOL3.root')
tf_NOL5         = r.TFile('files/NOL_NewAdditions/NOL5.root')

tfs = [ tf_Kurray, tf_NOL3, tf_NOL5 ]
titles = ['Kurray', 'NOL3', 'NOL5']
names = ['kurray','nol3','nol5']
trees = [ tf.Get('DetectedPhotons') for tf in tfs ]

compHist(trees,names,titles,'wavelength','#lambda (nm)','No. of detected photons',100,300,600,'_det')
compHist(trees,names,titles,'energy','Energy (MeV)','No. of detected photons',100,2,4,'_det')
compHist(trees,names,titles,'localtime','Local Time (ns)','No. of detected photons',100,0,20,'_det')
compHist(trees,names,titles,'abstime','Abs Time (ns)','No. of detected photons',100,0,25,'_det')
compHist(trees,names,titles,'length','length (mm)','No. of detected photons',100,0,4e3,'_det')

trees = [ tf.Get('ProducedPhotons') for tf in tfs ]

compHist(trees,names,titles,'wavelength','#lambda (nm)','No. of scintillation photons',100,300,600,'_scint','creatorProcess==1')
compHist(trees,names,titles,'energy','Energy (MeV)','No. of scintillation photons',100,2,4,'_scint','creatorProcess==1')
compHist(trees,names,titles,'localtime','Local Time (ns)','No. of scintillation photons',100,0,20,'_scint','creatorProcess==1')
compHist(trees,names,titles,'abstime','Abs Time (ns)','No. of scintillation photons',100,0,25,'_scint','creatorProcess==1')
compHist(trees,names,titles,'length','length (mm)','No. of scintillation photons',100,0,4e3,'_scint','creatorProcess==1')

trees = [ tf.Get('OpWlsPhotons') for tf in tfs ]

compHist(trees,names,titles,'wavelength','#lambda (nm)','No. of wls photons',100,300,600,'_wls')
compHist(trees,names,titles,'energy','Energy (MeV)','No. of wls photons',100,2,4,'_wls')
compHist(trees,names,titles,'localtime','Local Time (ns)','No. of wls photons',100,0,20,'_wls')
compHist(trees,names,titles,'abstime','Abs Time (ns)','No. of wls photons',100,0,25,'_wls')
compHist(trees,names,titles,'length','length (mm)','No. of wls photons',100,0,4e3,'_wls')

for tf in tfs:
  tf.Close()

tf_Kurray       = r.TFile('files/NOL_NewAdditions/out_Kurray.root')
tf_NOL3         = r.TFile('files/NOL_NewAdditions/out_NOL3.root')
tf_NOL5         = r.TFile('files/NOL_NewAdditions/out_NOL5.root')

tfs = [ tf_Kurray, tf_NOL3, tf_NOL5 ]
titles = ['Kurray', 'NOL3', 'NOL5']
names = ['kurray','nol3','nol5']
trees = [ tf.Get('outtree') for tf in tfs ]

compHist(trees,names, titles, 'nphos','No. of produced photons','Events',100,0,1000)
compHist(trees,names, titles, 'e_depos','Energy deposited (keV)','Events',100,0,200)
compHist(trees,names, titles, 'ndetphos','No. of detected photons','Events',50,0,50)

for tf in tfs:
  tf.Close()




