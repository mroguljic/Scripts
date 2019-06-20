import numpy as np
import matplotlib.pyplot as plt
import ROOT as r

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


fileList = [["phot1.root"], ["phot1p5.root"],["phot2.root"],
["phot2p5.root"],["phot3.root"]]

for rFile in fileList:
	f 				 = r.TFile.Open(rFile[0])
	print(rFile[0])
	hist			 = f.Get("dEdX")
	rFile.append([])
	for n in range(0,100):
		rFile[1].append(hist.GetBinContent(n))
	rFile.append(max(rFile[1]))

norm=1.05
for rFile in fileList:
	rFile[2]=norm/rFile[2]
	for i in range(len(rFile[1])):
		rFile[1][i]=rFile[1][i]*rFile[2]


#hist.GetNbinsX()
N          = 60
smoothing  = 15
lineStyles = ['-','-.','--',':','-']
labels	   = ["1 MeV", "1.5 MeV", "2 MeV", "2.5 MeV", "3 MeV"]
colors	   = ["blue","orange","black","green","red"]

x = np.arange(0,N/10.0,0.1)

for i in range(5):
	plt.plot(x,smooth(fileList[i][1][:N+smoothing],smoothing)[:-smoothing]
		,lineStyles[i], label=labels[i], color=colors[i])

plt.ylabel('Relative dose (A.U.)',fontsize=20)
plt.xlabel('Depth (mm)',fontsize=20)

plt.xticks(fontsize=14, rotation=0)
plt.yticks(fontsize=14, rotation=0)

plt.axis([0., N/10., 0, 1.])

plt.legend(prop={'size': 18})

plt.show()