#!/usr/bin/env python

import ROOT as r

def readExtinktionFile(tf):

  fil = open(tf)
  vals = []
  for line in fil.readlines():
    x = float(line.split()[0])
    y = float(line.split()[1])
    vals.append([x,y])

  vals.sort(key=lambda x: x[0])
  fil.close()
  return vals

def convExtinkToAbsorp(vals):

  new_vals=[]
  for val in vals:
    x = 1239.842/float(val[0])
    y = 1./(val[1]/100.)
    new_vals.append([x,y])

  new_vals.sort(key=lambda x: x[0])
  return new_vals

def valsToGraph(vals):

  gr = r.TGraph()
  for p, val in enumerate(vals):
    gr.SetPoint(p,val[0],val[1])
  return gr

def getFunc(fname):

  tf = open(fname)
  for i, line in enumerate(tf.readlines()):
    if i!=23: continue
    else: formula = line

  formula = formula.strip('\n')
  formula = formula.strip('\"')
  func = r.TF1('f',formula,200.,800.)
  tf.close()
  return func

def fit(gr,name):

  ft = r.TF1(name,"pol9",200,800)
  gr.Fit(ft,'RN')
  return ft

if_kurr_ext = '../../parameterFiles/TPBD_extinktion_1000ppm.csv'
if_nol3_ext  = 'NOL3_extinktion.csv'
if_nol5_ext  = 'NOL5_extinktion.csv'

vals_kur_ext  = readExtinktionFile(if_kurr_ext)
vals_nol3_ext = readExtinktionFile(if_nol3_ext)
vals_nol5_ext = readExtinktionFile(if_nol5_ext)

vals_kur_abs = convExtinkToAbsorp(vals_kur_ext)
vals_nol3_abs = convExtinkToAbsorp(vals_nol3_ext)
vals_nol5_abs = convExtinkToAbsorp(vals_nol5_ext)

gr_kur_abs = valsToGraph(vals_kur_abs)
gr_nol3_abs = valsToGraph(vals_nol3_abs)
gr_nol5_abs = valsToGraph(vals_nol5_abs)

gr_kur_abs.SetName("gr_kur_abs")
gr_nol3_abs.SetName("gr_nol3_abs")
gr_nol5_abs.SetName("gr_nol5_abs")
tf = r.TFile("outf.root","RECREATE")
gr_kur_abs.Write()
gr_nol3_abs.Write()
gr_nol5_abs.Write()
tf.Close()

func = getFunc('../../parameterFiles/parameters_Kurray.dat')

func.SetLineWidth(2)
func.SetLineColor(r.kBlack)
func.SetLineStyle(r.kDashed)

gr_kur_abs.SetLineWidth(2)
gr_nol3_abs.SetLineWidth(2)
gr_nol5_abs.SetLineWidth(2)
gr_kur_abs.SetLineColor(r.kBlue)
gr_nol3_abs.SetLineColor(r.kRed)
gr_nol5_abs.SetLineColor(r.kGreen+1)

#fit_nol3 = fit(gr_nol3_abs,'nol3')
#fit_nol5 = fit(gr_nol5_abs,'nol5')

"""
fit_nol3 = r.TF1('nol3','[0]*exp(-0.5*((x-[1])/[2])**2)+[3]*exp(-0.5*((x-[4])/[5])**2)+[6]*exp(-0.5*((x-[7])/[8])**2)+[9]*exp(-0.5*((x-[10])/[11])**2)+[12]*x+[13]+[14]*exp(-0.5*((x-[15])/[16])**2)+[17]*exp(-0.5*((x-[18])/[19])**2)',200,700)
fit_nol3.SetParameter(0,2.44213e+07)
fit_nol3.SetParameter(1,327.063)
fit_nol3.SetParameter(2,24.9213)
fit_nol3.SetParameter(3,3.49336e+07)
fit_nol3.SetParameter(4,256.983)
fit_nol3.SetParameter(5,8.84735)
fit_nol3.SetParameter(6,4.99405e+06)
fit_nol3.SetParameter(7,395.117)
fit_nol3.SetParameter(8,7.47301)
fit_nol3.SetParameter(9,4.589e+06)
fit_nol3.SetParameter(10,382.208)
fit_nol3.SetParameter(11,43.379)
fit_nol3.SetParameter(12,-260527)
fit_nol3.SetParameter(13,7.83e+07)
fit_nol3.SetParameter(14,4.58985e+06)
fit_nol3.SetParameter(15,382.208)
fit_nol3.SetParameter(16,43.3799)
fit_nol3.SetParameter(17,4.99405e+06)
fit_nol3.SetParameter(18,395.117)
fit_nol3.SetParameter(19,7.47301)
"""
#fit_nol3 = r.TF1('nol3','[0]* ( exp([1]*x) + [2]*exp(-0.5*((x-[3])/[4])) + [5]*exp(-0.5*((x-[6])/[7])) )',300,600)
#fit_nol3.SetParameter(0,5.e+05)
#fit_nol3.SetParameter(1,-0.16201)
#fit_nol3.SetParameter(2,5.)
#fit_nol3.SetParameter(3,354.544)
#fit_nol3.SetParameter(4,84.0782)
#fit_nol3.SetParameter(5,10.)
#fit_nol3.SetParameter(6,326.484)
#fit_nol3.SetParameter(7,26.2806)

#fit_nol3 = r.TF1('nol3','pol2(0) + gaus(3) + gaus(6) + gaus(9)',200,600)
#fit_nol3 = r.TF1('nol3','pol3',200,600)
#fit_nol3.SetParameter(0,-1.17266e+08)
#fit_nol3.SetParameter(1,1.511e+06)
#fit_nol3.SetParameter(2,-3996.26)
#fit_nol3.SetParLimits(0,-1.17266e+08,-1.17266e+08)
#fit_nol3.SetParLimits(1,1.511e+06,1.511e+06)
#fit_nol3.SetParLimits(2,-3996.26,-3996.26)

fit_nol3 = r.TF1('nol3','landau(0)+gaus(3)+gaus(6)',0,600)
fit_nol3.SetParameter(0,1.30721e+06)
fit_nol3.SetParameter(1,230.644)
fit_nol3.SetParameter(2,36.7123)
fit_nol3.SetParameter(3,3.49336e+07)
fit_nol3.SetParameter(4,256.983)
fit_nol3.SetParameter(5,8.84735)
fit_nol3.SetParameter(6,2.44213e+07)
fit_nol3.SetParameter(7,327.063)
fit_nol3.SetParameter(8,24.9213)
fit_nol3.SetParameter(9, -1.99339e+07)
fit_nol3.SetParameter(10,      619437)

#fit_nol3.SetParLimits(0,1.30721e+06,1.30721e+06)
fit_nol3.SetParLimits(1,230.644,230.644)
fit_nol3.SetParLimits(2,36.7123,36.7123)
#fit_nol3.SetParLimits(3,3.49336e+07,3.49336e+07)
fit_nol3.SetParLimits(4,256.983,256.983)
fit_nol3.SetParLimits(5,8.84735,8.84735)
#fit_nol3.SetParLimits(6,2.44213e+07,2.44213e+07)
fit_nol3.SetParLimits(7,327.063,327.063)
fit_nol3.SetParLimits(8,24.9213,24.9213)

prop_nol3 = r.TF1('nol3','1.3e+06*TMath::Landau(x,230.644,36.7123) + 3.5e+07*TMath::Gaus(x,257,8.84) + 2.44e+07*TMath::Gaus(x,327,24.9)',300,800)

prop_nol3.SetLineColor(r.kBlue)
prop_nol3.SetLineStyle(r.kDashed)
#gr_nol3_abs.Fit(fit_nol3,"RN")

mg = r.TMultiGraph()
#mg.Add(gr_kur_abs)
#mg.Add(gr_nol3_abs)
#mg.Add(gr_nol5_abs)

c = r.TCanvas()
#func.Draw("L")
#mg.Draw("Lsame")
gr_nol3_abs.Draw("AL")
prop_nol3.Draw("Lsame")
#fit_nol5.Draw("same")
c.Update()
c.Modified()

raw_input()



