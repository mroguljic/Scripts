import matplotlib.pyplot as plt


radius=[81,101,126,151,181]
mcDose=[299.387649,195.7588655,127.591068,89.870682,63.2213395]
measurementDose=[305.5,194.5,124.6,89.3,53.8]

mcPlot, = plt.plot(radius,mcDose,"ro",label="Monte-Carlo")
measurementPlot,     = plt.plot(radius,measurementDose,"bs",label="Measurements")

legend = plt.legend(handles=[mcPlot,measurementPlot],fontsize='x-large',framealpha=1.)

plt.xlabel('Distance from the cylinder [cm]',fontsize=20)
plt.ylabel('Dose rate [mGy/s]',fontsize=20)

plt.ylim(0,350)

plt.grid(True,which='both')
plt.savefig('scatterChangingR.pdf')


plt.show()