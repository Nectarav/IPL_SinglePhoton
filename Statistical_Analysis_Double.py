# PH2561: Single Photon
import numpy as np
import math
from matplotlib import pyplot as plt
from scipy import optimize

# Import the datasets you want to fit your data to. Depending on the column and the amount of header, you may have to
# Change the usecols and skip_header params. Remember that python indexes from zero, so the "first" column has index 0

XCOLUMN = 0
YCOLUMN = 1
# YCOLUMNERROR = 2
# XCOLUMNERROR = 3
NUMBEROFHEADERS = 1

xData = np.genfromtxt('Double_Slit_Data.csv', usecols=XCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')
yData = np.genfromtxt('Double_Slit_Data.csv', usecols=YCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')

# And of course, we need our error bars too. I made these up, but usually you would grab these from a column too.
# If you need X error bars as well, you can use the same method to get those. Just make sure you add in X error
# wherever you do Y error.
# yErr = np.genfromtxt('IPL-Nuclear-RawData.csv', usecols=YCOLUMNERROR, skip_header=NUMBEROFHEADERS, delimiter=',')
# xErr = np.genfromtxt('IPL-Nuclear-RawData.csv', usecols=XCOLUMNERROR, skip_header=NUMBEROFHEADERS, delimiter=',')

# Now the fun part, here is where we define the function we want to use to fit the data. We can define any type of
# function we want, with any number of parameters we want. I'll be using an exponential for my data, but you use whatever
# you have.

def f(x, A, B, C, D):
    return A * np.sinc(B * (x - 4.3675)) ** 2 * np.cos(np.pi * C * (x-4.3675)) ** 2 + D

# x is our dependent variable here, everything else is a parameter that scipy will decide for us.
# So, let's make scipy do that:

popt, pcov = optimize.curve_fit(f, xData, yData)

# Now, let's take a look at what "curve" is telling us:

print(popt, "\n\n\n", pcov)

# Looks a bit confusing. To break it down:
# There are two arrays that scipy will return, the first array is the more important one right now.
# This first array is the optimal values of the parameters you gave it, in the order you gave them.
# So in our example here, popt [0] is a and popt[1] is b.
# The second array is a 2d array of the covariance of the values in popt (your coefficients).
# This is a measure of how independent the two coefficient values are, but I will be ignoring it for the time being.
# We do want the r^2 values from this function though, so we'll go ahead and write a function to calculate that
# as well as pull out the residuals in the process.

residuals = yData - f(xData, *popt)
print("\n\nHere are the residuals: \n\n", residuals)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((yData-np.mean(yData))**2)
r_squared = 1 - (ss_res / ss_tot)

print("\n\nr^2 is: ", r_squared, "\n\n")
# Alright. We have all the data analysis done that we want. We can actually start graphing now!
# This next function will tell us where the curve fit should start, then where it should end, then how much each
# new point should increment by (resolution)
START = 0.05
END = 8.5
STEP = 0.1
x = np.arange(START, END, STEP)

# And we generate the y values of the fit by inserting the values we get from popt back into our chosen function.
# remember that python indexes from zero, unlike matlab, so the first constant you used in your definition of the
# function is going to be popt[0], the second will be popt[1], etc.

y = popt[0] * np.sinc(popt[1] * (x - 4.3675)) ** 2 * np.cos(np.pi * popt[2] * (x-4.3675)) ** 2 + popt[3]

# At this point, we're done. We have the x and y values of the fit. All that's left is to plot everything. Let's do it.
# The next few variables determine font sizes for things. Feel free to add more font size variables or change around how
# you want your graph to look. Playing with it is a good way to get more familiar with the tools you're using.
SMALL_SIZE = 13
MEDIUM_SIZE = 16
BIGGER_SIZE = 22

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('axes', titlesize=BIGGER_SIZE)

# A note here: There are a ton of types of plots you can use with matplotlib. For example, I often plot exponentials and
# thus I plot on semilog or log plots pretty frequently. plt.semilog() lets you do a semilog plot, and other commands
# will let you do a ton of other plot types!

# This one puts your actual data on the plot as a scatter plot
plt.plot(xData, yData, "o", marker=".", color='blue')
# This one puts the calculated fit onto the plot as a line.
FITLABEL = "placeholder"
plt.plot(x, y, color = 'blue', label=FITLABEL, linestyle = 'dotted')
# If you have error bars, you will want to uncomment this line below and use these error bars, changing color etc as
# appropriate
#plt.errorbar(xData, yData, yerr = yErr, xerr = xErr, color ='darkgreen', linestyle ='', capthick = 1, capsize = 1)
PLOTTITLE = "Voltage as a Function of Micrometer Position for a Single Slit Experiment (6.75mm)"
plt.title(PLOTTITLE)

# There are lots of legend locations, choose the one that looks best on your graph
plt.legend(loc = 7)
XLABEL = "Micrometer Position (mm)"
YLABEL = "Voltage (V)"
plt.xlabel(XLABEL)
plt.ylabel(YLABEL)
plt.show()

# Make sure you put your equation into your graph caption, or into your graph's legend, or SOMEWHERE in your report
# (legend or caption is preferable). Doing all
# this effort to curve fit and then not getting the equation into the report is a whole bunch of wasted effort.
# The parameters are what we did all this for. Not the funny line.