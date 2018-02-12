import numpy as np
from numpy import pi, r_
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

radius=[0.5,1.,1.5,2.,2.5,3.,3.5]
shieldingDose=[2.0577,1.0231,0.67753,0.50441,0.40308,0.33549,0.28692]

offPoint=[0.1,7.8284]

def powerFit(x, a, b):
		return a*np.power(x,b)

fit = curve_fit(powerFit,radius,shieldingDose)
parameters    = fit[0]
parametersErr = np.sqrt(np.diag(fit[1]))
print parameters
print parametersErr

pltRadii=np.linspace(0.1,4,100)
plt.plot(pltRadii,powerFit(pltRadii,parameters[0],parameters[1]))
plt.plot(radius,shieldingDose,"ro")
plt.plot(offPoint[0],offPoint[1],"ro")

plt.xscale('log')
plt.yscale('log')

plt.xticks([0.1,0.5,1.0,2,3,4],["0.1","0.5","1","2","3","4"])
plt.yticks([0.1,0.5,1.0,10.0],["0.1","0.5","1","10"])

plt.grid(True,which='both')

plt.xlabel('Water sphere radius [cm]',fontsize=20)
plt.ylabel('Shielding dose rate [Gy/s]',fontsize=20)

plt.savefig('ShieldingDoseFit.pdf')

plt.show()

