import ROOT as r
import numpy as np

rootFile = r.TFile('Profile.root')
tree     = rootFile.Get('DoseP')
nEvents  = tree.GetEntriesFast()
print nEvents, 'number of steps'

correctedFile = r.TFile('Corrected.root','RECREATE')
correctedTree = r.TTree("name","name")
updatedZ      = np.zeros(1,dtype=float)
updatedX      = np.zeros(1,dtype=float)
updatedY      = np.zeros(1,dtype=float)
updatedEDep   = np.zeros(1,dtype=float)
branchZ       = correctedTree.Branch('z',updatedZ,'z/D')
branchZ       = correctedTree.Branch('x',updatedX,'x/D')
branchZ       = correctedTree.Branch('y',updatedY,'y/D')
branchZ       = correctedTree.Branch('eDep',updatedEDep,'eDep/D')

for i,event in enumerate(tree):
  if(i%10000==0):
    print i

  z    = event.z
  x    = event.x
  y    = event.y
  preZ = event.preZ
  preX = event.preX
  preY = event.preY
  eDep = event.eDep

  postPos     = np.array([x,y,z])
  prePos      = np.array([preX,preY,preZ])
  track       = np.subtract(postPos,prePos)
  trackLen    = np.linalg.norm(track)
  direction   = track/trackLen

  if(prePos[2]<=0.):
    tempPos = prePos

  correctedStep  = np.add(np.random.exponential(trackLen)*direction,tempPos)
  updatedZ[0]    = correctedStep[2]
  updatedX[0]    = correctedStep[0]
  updatedY[0]    = correctedStep[1]
  updatedEDep[0] = eDep

  tempPos = correctedStep

  correctedTree.Fill()

correctedFile.Write()
correctedFile.Close()