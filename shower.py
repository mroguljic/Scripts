nLeptons=[0.]
nGammas=[1.]

nCascades=10
for i in xrange(nCascades):
	newLeptons= nGammas[i]*2
	newGammas = nLeptons[i]
	nLeptons.append(nLeptons[i]+newLeptons)
	nGammas.append(newGammas)

#print nLeptons
#print nGammas 

leptonLength=0.
totalLength=0.
for i,nLep in enumerate(nLeptons):
	leptonLength+=nLep
	totalLength+=nLep+nGammas[i]
	print 'Lepton tracks in radiation lengths = ', leptonLength
	print 'Total tracks in radiation lengths  = ', totalLength
	print 'Ratio = ', leptonLength/totalLength
	print '------------'