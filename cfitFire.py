# This script initiates curveFit.py.  

import curveFit
from os import path

print 'This program fit Gaussian distribution on chi plot data and return the height of peak found.'

done = False

while not done:
  filePath = curveFit.getFilePath()
  fileName = path.basename(filePath)[:-4]
  array = curveFit.readChi(filePath)
  differences = curveFit.PeakFinder(array)
  separation = curveFit.Periodicity(differences)
  curveFit.PeakFit(separation, array,fileName)
  ans = raw_input("Do you want to fit more chi plots in this session?(y or n): ")
  if ans == 'n':
    done = True
  
  
  
print 'Thank you! This program was written by Meng "Mamie" Wang. For more questions contact Mamie at mamie@hawk.iit.edu or Rama at ramasashank@gmail.com'

