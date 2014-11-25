## bloody constants and that
plank_c = 4.135667e-15 # eVs
light_c = 2.997925e17  # nm/s
nm_to_mev = (plank_c*light_c)

avoga_c = 6.022e23 # /mol
# from NOL paper = C = 1e-5 M = 1e-5 1000 mol/m^3 = 1e-3 mol / cm^3
mol_conc = 1.e-3   # mol/cm^3 (from NOL paper C=10^-5 M)
molecules_per_cm3 = avoga_c*mol_conc

print 'MOLS/cm3: ', molecules_per_cm3

##

import sys

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f","--filename")
parser.add_option("-x","--xrange",default="-1:-1")
parser.add_option("-y","--yrange",default="-1:-1")
parser.add_option("--log",default=False,action="store_true")
parser.add_option("-e","--energy",default=False,action="store_true")
(opts,args) = parser.parse_args()

f = open(opts.filename)

xrange = (float(opts.xrange.split(':')[0]),float(opts.xrange.split(':')[1]))
yrange = (float(opts.yrange.split(':')[0]),float(opts.yrange.split(':')[1]))

import ROOT as r

grWav = r.TGraph()
grEn = r.TGraph()
grInvAbsLength = r.TGraph()

wavps = []

for p,line in enumerate(f.readlines()):
	x = float(line.split(',')[0])
	y = float(line.split(',')[1])
	grWav.SetPoint(p,x,y)
	wavps.append( [nm_to_mev/x, y] )

wavps.sort(key=lambda x: x[0])

for p, wavp in enumerate(wavps):
	grEn.SetPoint(p,wavp[0],wavp[1])
	invabslength = wavp[1]*molecules_per_cm3
	grInvAbsLength.SetPoint(p,wavp[0],1./invabslength)


relGr = grWav
if opts.energy:
	relGr = grEn

if xrange[0]<0 and xrange[1]<0:
	xrange = ( relGr.GetXaxis().GetXmin() , relGr.GetXaxis().GetXmax() )

if yrange[0]<0 and yrange[1]<0:
	yrange = ( relGr.GetYaxis().GetXmin() , relGr.GetYaxis().GetXmax() )

dummy = r.TH1F('dum','',1,xrange[0],xrange[1])
dummy.GetYaxis().SetRangeUser(yrange[0],yrange[1])

dummy.GetXaxis().SetTitle("Wavelength (nm)")
if opts.energy:
	dummy.GetXaxis().SetTitle("Energy (eV)")

canv = r.TCanvas()
dummy.Draw()
if opts.energy:
	grEn.Draw("LPsame")
else:
	grWav.Draw("LPsame")
if opts.log:
	canv.SetLogy()
canv.Update()
canv.Modified()

canv2 = r.TCanvas()
grInvAbsLength.GetXaxis().SetTitle("Energy (eV)")
grInvAbsLength.GetYaxis().SetTitle("Absorption Length (cm)")
grInvAbsLength.Draw("ALP")
canv2.Update()
canv2.Modified()
raw_input()
