# PH2561: Single Photon
import numpy as np
import math
from matplotlib import pyplot as plt

XCOLUMN = 0
YCOLUMN = 1
YCOLUMNERROR = 2
NUMBEROFHEADERS = 1

# Constants
a = 0.085
d = 0.353
w = 0.000670

# Experimental double slit
xDoubleData = np.genfromtxt('Double_Slit_Data.csv', usecols=XCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')
yDoubleData = np.genfromtxt('Double_Slit_Data.csv', usecols=YCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')
yDoubleDataErr = np.genfromtxt('Double_Slit_Data.csv', usecols=YCOLUMNERROR, skip_header=NUMBEROFHEADERS, delimiter=',')

# Experimental right slit
xRightData = np.genfromtxt('6.75_Data.csv', usecols=XCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')
yRightData = np.genfromtxt('6.75_Data.csv', usecols=YCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')

# Experimental left slit
xLeftData = np.genfromtxt('4.82_Data.csv', usecols=XCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')
yLeftData = np.genfromtxt('4.82_Data.csv', usecols=YCOLUMN, skip_header=NUMBEROFHEADERS, delimiter=',')

# Theoretical double slit
def y_double_theory(x):
    theta = np.arctan((x-4.35)/500)
    return (411.67 *
            (np.cos(
                (np.pi * d) / (w)
                * np.sin(
                    np.atan(
                        theta
                    )
                )
            ) ** 2)
            * ((
                    (w * np.sin(
                        (np.pi * a) / (w) *
                        np.sin(np.atan(theta))
                    )
                     ) / (np.pi * a * np.sin(theta))
            ) ** 2)
            )

def y_left_theory(x):
    theta = np.arctan((x-5.36)/500)
    return (162.07 *
            ((
                    (w * np.sin(
                        (np.pi * a) / (w) *
                        np.sin(np.atan(theta))
                    )
                     ) / (np.pi * a * np.sin(theta))
            ) ** 2)
            )

def y_right_theory(x):
    theta = np.arctan((x-5.45)/500)
    return (118.87 *
            ((
                    (w * np.sin(
                        (np.pi * a) / (w) *
                        np.sin(np.atan(theta))
                    )
                     ) / (np.pi * a * np.sin(theta))
            ) ** 2)
            )

# Create double slit plot
fig, (ax1, ax2) = plt.subplots(1, 2, layout = 'constrained')
ax1.plot(xDoubleData, y_double_theory(xDoubleData), zorder = 1, label = 'Theoretical Data', color = 'orange')
ax1.scatter(xDoubleData, yDoubleData, zorder = 3, label = 'Experimental Data', color = 'blue', s=5)
ax1.errorbar(xDoubleData, yDoubleData, xerr = 0.01, yerr = yDoubleDataErr, zorder = 2, color = 'red', fmt = 'none')
ax1.set_title('Voltage as a function of Micrometer Position: Double Slit')
ax1.set_xlabel('Micrometer position (mm)')
ax1.set_ylabel('Voltage (mV)')
ax1.legend()

# Create single slit plots
ax2.plot()
ax2.scatter(xRightData, yRightData, zorder = 3, label = '6.75 slit experimental data', color = 'blue', s=5)
ax2.plot(xRightData, y_left_theory(xRightData), zorder = 1, label = '6.75 slit theoretical data', color = 'orange')
ax2.errorbar(xRightData, yRightData, xerr = 0.01, yerr = 0.23, zorder = 2, fmt = 'none', color = 'red')

ax2.scatter(xLeftData, yLeftData, zorder = 6, label = '4.82 slit experimental data', color = 'teal', s=5)
ax2.plot(xLeftData, y_left_theory(xLeftData), zorder = 4, label = '4.82 slit theoretical data', color = 'orange')
ax2.errorbar(xLeftData, yLeftData, xerr = 0.01, yerr = 0.31, zorder = 5, fmt = 'none', color = 'red')

ax2.set_title('Voltage as a function of Micrometer Position: Single Slit')
ax2.set_xlabel('Micrometer position (mm)')
ax2.set_ylabel('Voltage (mV)')
ax2.legend()
plt.show()