Run

1.)  python buildNOLspectra.py
2.)  python fit_absorp.py

1.) will output these files:

    NOL5_extinktion.csv
    NOL5_emission.csv
    NOL3_extinktion.csv
    NOL3_emission.csv

    these should then be added to parameters.dat for simulation

2.) will output two TFormulas like this:

    NOL3 =  (258.119 * TMath::Gaus(x,194.725,43.2183)) + (277.825 * TMath::Gaus(x,257.607,6.17715)) + (243.653 * TMath::Gaus(x,327.778,23.8381)) + (38.4452 * TMath::Gaus(x,394.708,10.1635))
    NOL5 =  (277.649 * TMath::Gaus(x,230.253,44.7654)) + (806.338 * TMath::Gaus(x,335.101,25.2355)) + (222.514 * TMath::Gaus(x,413.879,20.7173)) + (99.155 * TMath::Gaus(x,250.484,9.78525))

    these should then be added to current absoprtion (of polystyrene) formula in parameters.dat scaled by the 1-PLQY = 0.2
