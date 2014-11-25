#!/usr/bin/env python
import os
import ROOT as r
# PLQY from NOL paper
plqy = 0.8

#### useful constants ####
#plank_c = 4.135667e-15 # eVs
#light_c = 2.997925e17  # nm/s
#nm_to_ev = (plank_c*light_c)
nm_to_ev = 1239.842
avoga_c = 6.022e23 # /mol
# from NOL paper = C = 1e-5 M = 1e-5 1000 mol/m^3 = 1e-3 mol / cm^3
mol_conc = 1.e-8   # mol/cm^3 (from NOL paper C=10^-5 M)
molecules_per_cm3 = avoga_c*mol_conc
print 'MOLS/cm3: ', molecules_per_cm3

# outputfile
outf = r.TFile('NOLdata.root','RECREATE')

def readFile(fname,scale=1.):

  vals = []
  f = open(fname)
  for line in f.readlines():
    x = float(line.split()[0])
    y = float(line.split()[1])*scale
    print x, y
    vals.append([x,y])

  f.close()
  vals.sort(key=lambda x: x[0])
  return vals

def writeFile(fname, vals):

  f = open(fname,'w')
  for val in vals:
    line_out = '%5.3f %4.2E\n'%(val[0],val[1])
    f.write(line_out)
  f.close()

def convLamdaXStoEnergyLen(arr):

  vals=[]
  for val in arr:
    x = nm_to_ev/val[0]
    print val[0], val[1]
    y = (1./(val[1]*molecules_per_cm3) * plqy) / 100. # convert from cm to m
    vals.append([x,y])

  vals.sort(key=lambda x: x[0])
  return vals

def convLambdaIntesToEnergyIntes(arr):

  vals=[]
  for val in arr:
    x = nm_to_ev/val[0]
    y = val[1]
    vals.append([x,y])

  vals.sort(key=lambda x: x[0])
  return vals

def convEnergyLenToWavelengthInvLen(arr):

  vals=[]
  for val in arr:
    x = nm_to_ev/val[0]
    y = 1./val[1]
    vals.append([x,y])

  vals.sort(key=lambda x: x[0])
  return vals

def extendValues(values, isAbsorp, fLow=['pol1',150,227], fHigh=['expo',400,700]):

  new_vals = []
  values.sort(key=lambda x: x[0])
  # convert to graph
  grTemp = r.TGraph()
  for p, val in enumerate(values):
    grTemp.SetPoint(p,val[0],val[1])

  if isAbsorp:
    canv = r.TCanvas()
    fLow = r.TF1("fLow",fLow[0],fLow[1],fLow[2])
    fHigh = r.TF1("fHigh",fHigh[0],fHigh[1],fHigh[2])
    grTemp.Fit(fLow,"RN")
    grTemp.Fit(fHigh,"RN")
    grTemp.Draw("ALP")
    fLow.Draw("Lsame")
    fHigh.Draw("Lsame")
    canv.Update()
    canv.Modified()

  newValRange = [200,700]  # nm
  newValStep = 5          # nm
  npoints = (newValRange[1]-newValRange[0])/newValStep
  xlow = values[0][0]
  xhigh = values[-1][0]

  for p in range(npoints):
    xval = newValRange[0]+p*newValStep
    yval = grTemp.Eval(xval)

    if isAbsorp:
      if xval<xlow:
        yval = fLow.Eval(xval)
      elif xval>xhigh:
        yval = fHigh.Eval(xval)
      else:
        yval = grTemp.Eval(xval)
    else:
      if xval<xlow:
        yval = 0.
      elif xval>xhigh:
        yval = 0.
      else:
        yval = grTemp.Eval(xval)

    new_vals.append([xval,yval])

  new_vals.sort(key=lambda x: x[0])
  return new_vals

def makeGraph(points, name='', color=r.kBlack, xtitle='', ytitle=''):

  gr = r.TGraph()
  gr.SetName(name)
  gr.SetLineWidth(2)
  gr.SetLineColor(color)
  for p, point in enumerate(points):
    x = point[0]
    y = point[1]
    gr.SetPoint(p,x,y)
  gr.GetXaxis().SetTitleSize(0.05)
  gr.GetXaxis().SetLabelSize(0.05)
  gr.GetXaxis().SetTitleOffset(1.2)
  gr.GetYaxis().SetTitleSize(0.05)
  gr.GetYaxis().SetLabelSize(0.05)
  gr.GetYaxis().SetTitleOffset(1.2)
  gr.GetXaxis().SetTitle(xtitle)
  gr.GetYaxis().SetTitle(ytitle)
  outf.cd()
  gr.Write()
  return gr

def drawComp(grs_emiss, grs_absorp, name):

  canv = r.TCanvas("c","c",1800,1200)
  canv.Divide(3,2)
  for c in range(1,7):
    canv.GetPad(c).SetLeftMargin(0.15)
    canv.GetPad(c).SetBottomMargin(0.15)

  grs_absorp[0].GetYaxis().SetRangeUser(5.e-18,2.e-15)
  grs_absorp[1].GetYaxis().SetRangeUser(1.e-8,1.e15)
  grs_absorp[2].GetYaxis().SetRangeUser(1.e-8,1.e15)

  leg = r.TLegend(0.45,0.5,0.9,0.9)
  leg.SetFillColor(0)
  leg.AddEntry(grs_absorp[0],'NOL paper','L')
  leg.AddEntry(grs_absorp[1],'NOL Converted','L')
  leg.AddEntry(grs_absorp[2],'Kurray Nominal','L')

  for i, gr in enumerate(grs_emiss):
    canv.cd(i+1)
    gr.Draw("ALP")

  for i, gr in enumerate(grs_absorp):
    canv.cd(i+4)
    gr.Draw("ALP")

  canv.GetPad(4).SetLogy()
  canv.GetPad(5).SetLogy()
  canv.GetPad(6).SetLogy()
  leg.Draw("same")
  canv.Update()
  canv.Modified()
  canv.Print('%sdata.pdf'%name)

def drawAllExtink(grs):

  canv = r.TCanvas()
  grs[0].SetLineColor(r.kBlue)
  grs[1].SetLineColor(r.kRed)
  grs[2].SetLineColor(r.kGreen+1)
  leg = r.TLegend(0.55,0.6,0.9,0.9)
  leg.AddEntry(grs[0],'NOL3','L')
  leg.AddEntry(grs[1],'NOL5','L')
  leg.AddEntry(grs[2],'Kurray','L')
  mg = r.TMultiGraph()
  mg.Add(grs[0])
  mg.Add(grs[1])
  mg.Add(grs[2])
  mg.Draw("AL")
  mg.GetXaxis().SetTitle('Energy (eV)')
  mg.GetYaxis().SetTitle('Absoprtion Length (m)')
  mg.GetYaxis().SetRangeUser(1.e-8,1.e15)
  leg.Draw("same")
  canv.SetLogy()
  canv.Update()
  canv.Modified()
  canv.Print("extinktion.pdf")

def drawAllEmiss(grs):

  canv = r.TCanvas()
  grs[0].SetLineColor(r.kBlue)
  grs[1].SetLineColor(r.kRed)
  grs[2].SetLineColor(r.kGreen+1)
  leg = r.TLegend(0.1,0.6,0.3,0.9)
  leg.AddEntry(grs[0],'NOL3','L')
  leg.AddEntry(grs[1],'NOL5','L')
  leg.AddEntry(grs[2],'Kurray','L')
  mg = r.TMultiGraph()
  mg.Add(grs[0])
  mg.Add(grs[1])
  mg.Add(grs[2])
  mg.Draw("AL")
  mg.GetXaxis().SetTitle('Energy (eV)')
  mg.GetYaxis().SetTitle('Intensity (%)')
  mg.GetXaxis().SetRangeUser(1.5,5.)
  leg.Draw("same")
  canv.Update()
  canv.Modified()
  canv.Print("emission.pdf")

def drawAbsorp(grs, fits):

  canv = r.TCanvas()
  grs[0].SetLineColor(r.kBlue)
  grs[1].SetLineColor(r.kRed)
  grs[0].SetLineStyle(r.kDashed)
  grs[1].SetLineStyle(r.kDashed)
  fits[0].SetLineStyle(r.kBlue-7)
  fits[1].SetLineColor(r.kRed-7)
  fits[0].SetLineWidth(3)
  fits[1].SetLineWidth(3)
  leg = r.TLegend(0.1,0.6,0.3,0.9)
  leg.AddEntry(grs[0],'NOL3','L')
  leg.AddEntry(grs[1],'NOL5','L')
  mg = r.TMultiGraph()
  mg.Add(grs[0])
  mg.Add(grs[1])
  mg.Draw("AL")
  fits[0].Draw("Lsame")
  fits[1].Draw("Lsame")
  mg.GetXaxis().SetTitle("Wavelength (nm) ")
  mg.GetYaxis().SetTitle("Inv absorption length (m^{-1})")
  leg.Draw("same")
  canv.Update()
  canv.Modified()
  canv.Print("invabs.pdf")

def attemptFit(gr, fitfunc=""):

  ftest1 = r.TF1('ftest1','gaus(0)',300,365)
  gr.Fit(ftest1)
  ftest2 = r.TF1('ftest2','gaus(0)',380,450)
  gr.Fit(ftest2)

  if fitfunc=="":
    fit = r.TF1('f_%s'%gr.GetName(),'pol1(0) + gaus(2) + gaus(5) + gaus(8)',300,800)
    fit.SetParameter(3,ftest1.GetParameter(1))
    fit.SetParameter(2,ftest1.GetParameter(2))
  else:
    fit = r.TF1('f_%s'%gr.GetName(),fitfunc,300,800)

  gr.Fit(fit,"RN")
  return fit

# main
# input files
if_NOL3_absxs = 'NOL3_abs_in.csv'
if_NOL5_absxs = 'NOL5_abs_in.csv'
if_NOL3_emiss = 'NOL3_emission_in.csv'
if_NOL5_emiss = 'NOL5_emission_in.csv'

# output files
of_NOL3_extink = 'NOL3_extinktion.csv'
of_NOL5_extink = 'NOL5_extinktion.csv'
of_NOL3_emiss  = 'NOL3_emission.csv'
of_NOL5_emiss  = 'NOL5_emission.csv'

# Kurray files
if_Kurray_emiss  = '../../parameterFiles/p-Terphenyl_emission.csv'
if_Kurray_extink = '../../parameterFiles/TPBD_extinktion_1000ppm.csv'

# read values
vals_NOL3_absxs = readFile(if_NOL3_absxs)
vals_NOL5_absxs = readFile(if_NOL5_absxs)
vals_NOL3_emiss = readFile(if_NOL3_emiss,100.)
vals_NOL5_emiss = readFile(if_NOL5_emiss,100.)

# extend values
vals_NOL3_absxs = extendValues(vals_NOL3_absxs,True,['pol1',150,227], ['expo',400,700])
vals_NOL5_absxs = extendValues(vals_NOL5_absxs,True,['pol1',150,250], ['expo',450,700])
#vals_NOL3_emiss = extendValues(vals_NOL3_emiss,False)
#vals_NOL5_emiss = extendValues(vals_NOL5_emiss,False)

# convert into out units
cvals_NOL3_extink = convLamdaXStoEnergyLen(vals_NOL3_absxs)
cvals_NOL5_extink = convLamdaXStoEnergyLen(vals_NOL5_absxs)
cvals_NOL3_emiss  = convLambdaIntesToEnergyIntes(vals_NOL3_emiss)
cvals_NOL5_emiss  = convLambdaIntesToEnergyIntes(vals_NOL5_emiss)
cvals_NOL3_absorp = convEnergyLenToWavelengthInvLen(cvals_NOL3_extink)
cvals_NOL5_absorp = convEnergyLenToWavelengthInvLen(cvals_NOL5_extink)

# get equivalent for Kurray
cvals_Kurray_extink = readFile(if_Kurray_extink)
cvals_Kurray_emiss  = readFile(if_Kurray_emiss)

# turn into graphs
gr_NOL3_absxs      = makeGraph(vals_NOL3_absxs,     'NOL3_absoprtion_raw',    r.kRed,     'Wavelength (nm)', 'Absorption Cross Section (cm^{2})' )
gr_NOL3_extink     = makeGraph(cvals_NOL3_extink,   'NOL3_absorption_conv',   r.kBlue,    'Energy (eV)',     'Absorption Length (m)')
gr_NOL3_emiss_raw  = makeGraph(vals_NOL3_emiss,     'NOL3_emission_raw',      r.kRed,     'Wavelength (nm)', 'Intensity (%)')
gr_NOL3_emiss      = makeGraph(cvals_NOL3_emiss,    'NOL3_emission_conv',     r.kBlue,    'Energy (eV)',     'Intensity (%)')
gr_NOL3_invabs     = makeGraph(cvals_NOL3_absorp,   'NOL3_inv_absorption',    r.kMagenta, 'Wavelength (nm)', 'Inverse absoption length (m^{-1})')

gr_NOL5_absxs      = makeGraph(vals_NOL5_absxs,     'NOL5_absoprtion_raw',    r.kRed,     'Wavelength (nm)', 'Absorption Cross Section (cm^{2})' )
gr_NOL5_extink     = makeGraph(cvals_NOL5_extink,   'NOL5_absorption_conv',   r.kBlue,    'Energy (eV)',     'Absorption Length (m)')
gr_NOL5_emiss_raw  = makeGraph(vals_NOL5_emiss,     'NOL5_emission_raw',      r.kRed,     'Wavelength (nm)', 'Intensity (%)')
gr_NOL5_emiss      = makeGraph(cvals_NOL5_emiss,    'NOL5_emission_conv',     r.kBlue,    'Energy (eV)',     'Intensity (%)')
gr_NOL5_invabs     = makeGraph(cvals_NOL5_absorp,   'NOL5_inv_absorption',    r.kMagenta, 'Wavelength (nm)', 'Inverse absoption length (m^{-1})')

gr_Kurray_extink   = makeGraph(cvals_Kurray_extink, 'Kurray_absoprtion_std',  r.kGreen+1, 'Energy (eV)',     'Absorption Length (m)')
gr_Kurray_emiss    = makeGraph(cvals_Kurray_emiss,  'Kurray_emission_std',    r.kGreen+1, 'Energy (eV)',     'Intensity (%)')

# draw graphs
drawComp([gr_NOL3_emiss_raw, gr_NOL3_emiss, gr_Kurray_emiss] , [gr_NOL3_absxs,gr_NOL3_extink,gr_Kurray_extink] , 'NOL3')
drawComp([gr_NOL5_emiss_raw, gr_NOL5_emiss, gr_Kurray_emiss] , [gr_NOL5_absxs,gr_NOL5_extink,gr_Kurray_extink] , 'NOL5')

drawAllExtink( [gr_NOL3_extink, gr_NOL5_extink, gr_Kurray_extink] )
drawAllEmiss(  [gr_NOL3_emiss,  gr_NOL5_emiss,  gr_Kurray_emiss]  )

# write the files out
writeFile(of_NOL3_extink, cvals_NOL3_extink)
writeFile(of_NOL5_extink, cvals_NOL5_extink)
writeFile(of_NOL3_emiss,  cvals_NOL3_emiss)
writeFile(of_NOL5_emiss,  cvals_NOL5_emiss)

# now draw stuff to be fitted
fit_NOL3 = attemptFit(gr_NOL3_invabs)
fit_NOL5 = attemptFit(gr_NOL5_invabs)
drawAbsorp( [gr_NOL3_invabs, gr_NOL5_invabs] , [fit_NOL3, fit_NOL5] )

outf.Close()
