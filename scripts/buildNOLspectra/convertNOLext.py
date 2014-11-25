import ROOT as r

fin = open('NOL_extinktion.csv')
fout = open('NOL_extinktion_conv.csv','w')

gr = r.TGraph()

p=0
for line in fin.readlines():
  gr.SetPoint(p,float(line.split()[0]),float(line.split()[1]))
  p+=1

import numpy

arr = numpy.arange(1.900,4.4300,0.025)
for val in arr:
  fout.write('%6.4f %.2g\n'%(val,gr.Eval(val)))

fin.close()
fout.close()
