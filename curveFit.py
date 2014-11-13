# This program locates the peaks from the 2-theta vs intensity plots from Fit2D 
#   and fit normal distribution on individual peaks. An output file containing peak
#   height and center is output as a csv file and the plot of peaks is output
#   in png format.

# ========================================================================= #

# This function asks user for input file path and returns the file path if valid.
def getFilePath():
    import os
    getPath = False
    filePath = raw_input('Please enter the absolute path of your file:')
    
    while not getPath:
        if os.path.isdir(filePath):
            filePath += '/' + raw_input('...')
        elif os.path.isfile(filePath):
            print 'file found: ' + filePath
            getPath = True 
        elif not os.path.exists(filePath):
            filePath = raw_input('File path is not valid. Please input again:')
            
    return filePath

# ========================================================================= #
# File transfer and naming section. 
# This function reads the contents of chi file and converts the content to a
# array with rank two with dtype float64 (a two dimensional array). A csv 
# file containing only the data from chi file (without the header) is output 
# for next step. THIS FUNCTION DOES NOT DO THE FITTING YET. 

def readChi(filePath):
  
#    from time import strftime, gmtime (Uncomment this line if you want to use timestamp on output file name)    

    from csv import writer
    from numpy import array
    from os import path

    # outFileName = 'csv_'+ path.basename(filePath)[:-4] + '.csv' # Add this part of statement to output filename with Timestamp  
								    # + '_' + strftime("%b%d%H%M",gmtime())
    with open(filePath,'rb') as infile: #, open(outFileName, 'wb') as outfile: #Uncomment this to write out temp csv file. See below.
	lines_after_4 = infile.readlines()[4:]
	Text = lines_after_4
	k = [row.split() for row in Text]
	# writer = writer(outfile) These lines are for writing out a csv file after removing the header from the chiplot. 
	# for row in k:
	#	writer.writerow(row)
	#print 'The data for chi plot has been output to ' + outFileName + ' in current directory.'
        array = array(k).astype(float)
        return array

# ========================================================================= #

# This functions locates the local maxima based on information from the array created above.

def PeakFinder(array):
    x = array[:,0]
    y = array[:,1]
    from scipy import signal
    import numpy as np
    maxima = signal.find_peaks_cwt(y, np.arange(1,10)) # Working of this algorithm found in the following link
							# http://bioinformatics.oxfordjournals.org/content/22/17/2059.long
    difference = np.diff(maxima)			# This generates an array of differences between the indices of the 
							# local maxima which will be used below to find periodicity.
    return difference
    
# ========================================================================= #

# This function asks the user to estimate the periodicity in the data. The estimate can be made from the 
# frequency array of possible separation distances displayed in decreasing order of no. of occurences.

def Periodicity(differences):

    from collections import Counter

    data = Counter(differences)
    print 'Here is a frequency array of possible separation distances sorted in decreasing order by no. of occurences: ' 
    print ', '.join(map(str, data.most_common()))
    separation = int(raw_input('Please enter the most possible separation. Choose from above or from original data: '))
    
    return separation
    
# ======================================================================== #

# Defining a Gaussian distribution. 

def GaussianModel(x, sigma, center, A, C):
    import numpy as np
    return [A * np.exp(-(a - center)**2/(2 * sigma**2)) + C for a in x]

# ========================================================================= #

# This function fits peaks located periodically with Gaussian distribution (defined above)
# and plots the respective fitted peaks.

def PeakFit(separation, array, fileName):
    import numpy as np
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    from math import floor
    from csv import writer
    from os import path
    from time import strftime, localtime
    
    x = array[:,0]  # 2-theta or radial distance. Refer to Fit2D output (chi plot).
    y = array[:,1] # intensity from Fti2D output (chi plot).
    
    done = False
    while not done:
      n = int(raw_input('Please enter the number of peaks to fit: ')) #ADD RAISE EXCEPTION FOR DATA OUT OF BOUND ???????
      if(len(x) < n * separation):
        print ('Index out of bound. Input a smaller value.')
      else:
	 done = True

	 
#    sigma = int(raw_input('Please the half maximum width of peaks to fit: '))

    center = []           # placeholders
    height = []
    popt_array = [["sigma","center","height","baseline"]]
    
    for i in range(n):
        center.append(x[separation * (i + 1)]) # Defining starting point for peak fits. 
        height.append(y[separation * (i + 1)]) # Defining starting point for peak fits.
#    print center # For Debugging. 
#    print height # For Debugging.
    print 'sigma              mu                  height               baseline'
    for i in range(n):
        xdata = x[i*separation + int(floor(0.5 * separation)) : (i + 2) * separation- int(floor(0.5 * separation))] # defining the X-range of the peak.
        ydata = y[i*separation + int(floor(0.5 * separation)): (i + 2) * separation - int(floor(0.5 * separation))] # defining the Y-range of the peak.
                
        par = [0.01, center[i], height[i], 50] # Random initialization of Gaussian fit function. 
						# The 4 parameters correspond to sigma, center, A and C in function definition in line 88.
        popt, pcov = curve_fit(GaussianModel,xdata, ydata, par) # popt is the optimum set of parameters for the Gaussian fit. 
	                                                        # pcov is the covariance of the parameters. (not using in our case)
	popt_array.append(popt)                                 # writing popt to list to make a csv file with fit parameters and data. 
	
        print popt
        plt.close() # Closing any other program/script/loop using the plt library from line 100.
        plt.figure()
        plt.plot(xdata, ydata) # Plotting raw data.
        plt.plot(np.arange(min(xdata),max(xdata),0.001), GaussianModel(np.arange(min(xdata),max(xdata),0.001), *popt)) # Plotting fit data. 
        plt.savefig(fileName+'peak_'+str(i+1)+'.png') # Saving peak fit plot and raw peak plot as overlaid png.
    plt.close() 

    outFileName = 'fitted_'+ fileName + '_' + strftime("%b%d%H%M",localtime()) +'.csv' 
								    # 
    with open(outFileName, 'wb') as outfile: 
		
	writer = writer(outfile) # These lines are for writing out a csv file after removing the header from the chiplot. 
	for row in popt_array:
	  writer.writerow(row)
	print 'The fit data has been output to ' + outFileName + ' in current directory.'

# ========================================================================= #

'''print 'This program fit Gaussian distribution on chi plot data and return the height of peak found.'


filePath = getFilePath()
array = readChi(filePath)
differences = PeakFinder(array)
separation = Periodicity(differences)
PeakFit(separation, array)

print 'Thank you!'
'''
