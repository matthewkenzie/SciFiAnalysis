#!/usr/bin/env python

import ROOT as r

r.gROOT.ProcessLine(".x /Users/matt/Scratch/lhcb/lhcbStyle.C")

tf = r.TFile("NOLdata.root")

nol3_abs = tf.Get("NOL3_inv_absorption")
nol5_abs = tf.Get("NOL5_inv_absorption")

nol3_abs.GetXaxis().SetTitle('Wavelength (nm)')
nol3_abs.GetYaxis().SetTitle('Absorption coefficient (m^{-1})')
nol3_abs.GetXaxis().SetTitleOffset(0.8)
nol3_abs.GetYaxis().SetTitleOffset(0.8)
nol3_abs.GetXaxis().SetTitleSize(0.8*nol3_abs.GetXaxis().GetTitleSize())
nol3_abs.GetYaxis().SetTitleSize(0.8*nol3_abs.GetYaxis().GetTitleSize())

nol5_abs.GetXaxis().SetTitle('Wavelength (nm)')
nol5_abs.GetYaxis().SetTitle('Absorption coefficient (m^{-1})')
nol5_abs.GetXaxis().SetTitleOffset(0.8)
nol5_abs.GetYaxis().SetTitleOffset(0.8)
nol5_abs.GetXaxis().SetTitleSize(0.8*nol5_abs.GetXaxis().GetTitleSize())
nol5_abs.GetYaxis().SetTitleSize(0.8*nol5_abs.GetYaxis().GetTitleSize())

canvs = []

def printGraph(gr):
  print gr.GetName()
  x = r.Double()
  y = r.Double()
  for p in range(gr.GetN()):
    gr.GetPoint(p,x,y)
    print '\t', '%-3d'%p, ' - ', x ,' , ', y
  print '------------------------------------'

def fitNOL3(nol3_abs):

  canvs.append(r.TCanvas('nol3','nol3'))

  nol3_abs.SetMarkerSize(1.5)
  nol3_abs.SetMarkerColor(r.kBlack)
  nol3_abs.SetMarkerStyle(r.kFullCircle)
  nol3_abs.Draw("AP")

  tf_gaus1 = r.TF1('fgaus1','gaus',200,240)
  tf_gaus1.SetLineWidth(2)
  tf_gaus1.SetLineColor(r.kRed)
  nol3_abs.Fit(tf_gaus1,"RN")

  tf_gaus2 = r.TF1('fgaus2','gaus',240,280)
  tf_gaus2.SetLineWidth(2)
  tf_gaus2.SetLineColor(r.kRed)
  tf_gaus2.SetParameter(0,321.447)
  tf_gaus2.SetParameter(1,255.757)
  tf_gaus2.SetParameter(2,11.5745)
  nol3_abs.Fit(tf_gaus2,"RN")

  tf_gaus3 = r.TF1('fgaus3','gaus',280,380)
  tf_gaus3.SetParameter(0,242.93)
  tf_gaus3.SetParameter(1,326.685)
  tf_gaus3.SetParameter(2,25.5642)
  tf_gaus3.SetLineWidth(2)
  tf_gaus3.SetLineColor(r.kRed)
  nol3_abs.Fit(tf_gaus3,"RN")

  tf_gaus4 = r.TF1('fgaus4','gaus',380,600)
  tf_gaus4.SetLineWidth(2)
  tf_gaus4.SetLineColor(r.kRed)
  nol3_abs.Fit(tf_gaus4,"RN")

  #tf_gaus1.Draw("Lsame")
  #tf_gaus2.Draw("Lsame")
  #tf_gaus3.Draw("Lsame")
  #tf_gaus4.Draw("Lsame")

  tf_comb = r.TF1("comb","fgaus1+fgaus2+fgaus3+fgaus4",200,800)
  tf_comb.SetLineWidth(3)
  tf_comb.SetLineColor(r.kBlue)
  nol3_abs.Fit(tf_comb)
  tf_comb.Draw("same")

  form_str = ''

  for g in range(4): # nGaussians

    form_str += '(%g * TMath::Gaus(x,%g,%g))'%(tf_comb.GetParameter(3*g),tf_comb.GetParameter((3*g)+1),tf_comb.GetParameter((3*g)+2))
    if g!=3:
      form_str += ' + '

  print form_str
  tf_check = r.TF1("check",form_str,200,600)
  tf_check.SetLineWidth(3)
  tf_check.SetLineColor(r.kGreen+1)
  tf_check.SetLineStyle(r.kDashed)
  tf_check.Draw("same")

  canvs[-1].Update()
  canvs[-1].Modified()

  canvs[-1].Print("nol3_abs_fit.pdf")

  return form_str

def fitNOL5(nol5_abs):

  canvs.append( r.TCanvas('nol5','nol5'))

  nol5_abs.SetMarkerSize(1.5)
  nol5_abs.SetMarkerColor(r.kBlack)
  nol5_abs.SetMarkerStyle(r.kFullCircle)
  nol5_abs.Draw("AP")

  tf_gaus1 = r.TF1('fgaus1','gaus',200,270)
  tf_gaus1.SetLineWidth(2)
  tf_gaus1.SetLineColor(r.kRed)
  nol5_abs.Fit(tf_gaus1,"RN")

  tf_gaus2 = r.TF1('fgaus2','gaus',280,380)
  tf_gaus2.SetLineWidth(2)
  tf_gaus2.SetLineColor(r.kRed)
  tf_gaus2.SetParameter(0,321.447)
  tf_gaus2.SetParameter(1,255.757)
  tf_gaus2.SetParameter(2,11.5745)
  nol5_abs.Fit(tf_gaus2,"RN")

  tf_gaus3 = r.TF1('fgaus3','gaus',380,600)
  tf_gaus3.SetParameter(0,242.93)
  tf_gaus3.SetParameter(1,326.685)
  tf_gaus3.SetParameter(2,25.5642)
  tf_gaus3.SetLineWidth(2)
  tf_gaus3.SetLineColor(r.kRed)
  nol5_abs.Fit(tf_gaus3,"RN")

  tf_gaus4 = r.TF1('fgaus4','gaus',200,270)
  tf_gaus4.SetLineWidth(2)
  tf_gaus4.SetLineColor(r.kRed)
  nol5_abs.Fit(tf_gaus4,"RN")

  #tf_gaus1.Draw("Lsame")
  #tf_gaus2.Draw("Lsame")
  #tf_gaus3.Draw("Lsame")
  #tf_gaus4.Draw("Lsame")

  tf_comb = r.TF1("comb","fgaus1+fgaus2+fgaus3+fgaus4",200,800)
  tf_comb.SetLineWidth(3)
  tf_comb.SetLineColor(r.kBlue)
  nol5_abs.Fit(tf_comb)
  tf_comb.Draw("same")

  form_str = ''

  for g in range(4): # nGaussians

    form_str += '(%g * TMath::Gaus(x,%g,%g))'%(tf_comb.GetParameter(3*g),tf_comb.GetParameter((3*g)+1),tf_comb.GetParameter((3*g)+2))
    if g!=3:
      form_str += ' + '

  print form_str
  tf_check = r.TF1("check",form_str,200,600)
  tf_check.SetLineWidth(3)
  tf_check.SetLineColor(r.kGreen+1)
  tf_check.SetLineStyle(r.kDashed)
  tf_check.Draw("same")

  canvs[-1].Update()
  canvs[-1].Modified()

  canvs[-1].Print("nol5_abs_fit.pdf")

  return form_str

def getNominalFitString():
  tf = open("../../parameterFiles/parameters_Kurray.dat")
  formula = ''
  for i, line in enumerate(tf.readlines()):
    if i!=22: continue
    else: formula = line

  tf.close()
  formula = formula.strip('\n')
  formula = formula.strip('\"')
  return formula

def plotComparison(name,nolFitString, nominalFitString, fullFitString):

  canvs.append(r.TCanvas())
  nolf = r.TF1(name,'0.2*('+nolFitString+')',300,800)
  nomf = r.TF1('nom',nominalFitString,300,800)
  fullf = r.TF1(name+'full', fullFitString, 300, 800)

  nolf.SetLineColor(r.kGreen+2)
  nomf.SetLineColor(r.kRed)
  fullf.SetLineColor(r.kBlue)

  nolf.SetLineWidth(2)
  nolf.SetLineStyle(7)
  nomf.SetLineWidth(2)
  nomf.SetLineStyle(7)
  fullf.SetLineWidth(2)

  nolf.SetLineWidth(3)
  nomf.SetLineWidth(3)
  fullf.SetLineWidth(3)

  leg = r.TLegend(0.6,0.6,0.89,0.89)
  leg.AddEntry(nolf,name,'L')
  leg.AddEntry(nomf,'Polystyrene','L')
  leg.AddEntry(fullf,'Total','L')

  fullf.GetXaxis().SetTitle("Wavelength (nm) ")
  fullf.GetYaxis().SetTitle("Absorption coefficient (m^{-1})")
  fullf.GetXaxis().SetTitleOffset(0.8)
  fullf.GetYaxis().SetTitleOffset(0.8)
  fullf.GetXaxis().SetTitleSize(0.8*fullf.GetXaxis().GetTitleSize())
  fullf.GetYaxis().SetTitleSize(0.8*fullf.GetYaxis().GetTitleSize())

  fullf.Draw()
  nomf.Draw("same")
  nolf.Draw("same")
  leg.Draw("same")

  canvs[-1].SetLogy()

  canvs[-1].Modified()
  canvs[-1].Update()
  canvs[-1].Print(name+"full.pdf")

# main()

printGraph(nol3_abs)
printGraph(nol5_abs)

nol3fitString = fitNOL3(nol3_abs)
nol5fitString = fitNOL5(nol5_abs)
nominalfitString = getNominalFitString()

print '============ FITS DONE ============='
print 'NOL3 = ', nol3fitString
print 'NOL5 = ', nol5fitString
print '===================================='

nol3FullString = '(' + nominalfitString + ') + 0.2*(' + nol3fitString +')'
nol5FullString = '(' + nominalfitString + ') + 0.2*(' + nol5fitString +')'

plotComparison('NOL3', nol3fitString, nominalfitString, nol3FullString)
plotComparison('NOL5', nol5fitString, nominalfitString, nol5FullString)

print '=========== FULL STRING ============'
print 'NOL3 = ', nol3FullString
print 'NOL5 = ', nol5FullString
print '===================================='

raw_input('Happy?')
