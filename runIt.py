#!/usr/bin/env python

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d","--dir")
parser.add_option("-f","--filematch",default="*.root")
parser.add_option("-n","--nol",default=False,action="store_true")
(opts,args) = parser.parse_args()

import sys

import ROOT as r
r.gSystem.Load("lib/libAnalysis")
r.gROOT.SetBatch()

diams = set()
lengths = set()
fileDict = {}

import os
import fnmatch

if opts.nol:

  """
  fileDict= { 'Kurray': [], 'NOL': [] }
  for root, dirs, files in os.walk(opts.dir):
    print root, dirs, files
    for f in fnmatch.filter(files,opts.filematch):
      print f
      if 'Kurray' in f:
        fileDict['Kurray'].append(opts.dir+'/'+f)
      if 'NOL' in f:
        fileDict['NOL'].append(opts.dir+'/'+f)
  """

  fileDict = {

        'Kurray': [
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j0.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j1.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j2.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j3.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j4.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j5.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j6.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j7.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j8.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/Kurray_j9.root'
          ],
        'NOL3':    [
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j0.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j1.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j2.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j3.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j4.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j5.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j6.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j7.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j8.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL3_j9.root'
          ],
        'NOL5':    [
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j0.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j1.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j2.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j3.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j4.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j5.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j6.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j7.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j8.root',
              '~/eos/lhcb/user/m/mkenzie/SFT/Simulations/NOL_jobs_NewAdditions/NOL5_j9.root'
          ]
        }

  for fibre, fs in fileDict.items():
    print fibre
    analyser = r.AnalyseTrees()
    for f in fs:
      analyser.addFile(f,0.25,110)
    analyser.init('out_%s.root'%fibre,'outtree')
    analyser.run()
    analyser.fill()
    analyser.save()

else:

  for root, dirs, files in os.walk(opts.dir):
    for f in fnmatch.filter(files,opts.filematch):
      f_diam = float(f.split('_')[1].split('mm')[0])
      f_length = float(f.split('_')[3].split('cm')[0])
      key = (f_diam, f_length)
      print key, f
      if key not in fileDict.keys():
        fileDict[key] = [ '%s/%s'%(opts.dir,f) ]
      else:
        fileDict[key].append( '%s/%s'%(opts.dir,f) )

  for (diam,length), files in fileDict.items():

    print 'diam:', diam, 'length', length
    a = raw_input('Continue?')
    if a=='n' or a=='N' or a=='no' or a=='No':
      continue
    analyser = r.AnalyseTrees()
    for f in files:
      analyser.addFile(f,diam,length)
      print 'Added file', f, ' with diam', diam, 'and length', length
    analyser.init("out_d%4.2f_l%3.1f.root"%(diam,length),"outtree")
    analyser.run()
    analyser.fill()
    analyser.save()
