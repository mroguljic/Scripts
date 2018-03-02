from readData import readParams
from array import array
import ROOT as r


def getParam(measurements,doses,moduleTags,parameter):
#returns dictionary with moduleTags for keys and a list of requested parameter values for different doses
#params available so far: par0ia,par1ia,par2ia,par0vd,par1vd,par0va,par1va,Vbg
#also contains the list of doses used in the calculations with the key 'doses', result['doses']

#measurements should be a dictionary with this structure measurements[dose][tag][param]
#doses a list of doses we wish to get params for, i.e. doses= [0,2,4,8,17,34]


    result= {}
    result['doses'] = doses
    for tag in moduleTags:
        tempValues = []
        for dose in doses:
            tempValues.append(measurements[dose][tag][parameter])
        result[tag] = tempValues
    return result


def multiPlot(measurements,doses,moduleTags,parameter,name='multiPlot',title='multiPlot',outputFile='test.pdf'):
#input is the same as in getParam
#makes a multigraph param vs dose for requested moduleTags
    r.gROOT.SetBatch(1)
    c1 = r.TCanvas(name,title,200,10,700,500);
    c1.SetGrid();
    multiGr = r.TMultiGraph()
    leg = r.TLegend(0.1,0.7,0.25,0.9);


    values = getParam(measurements,doses,moduleTags,parameter)
    for eNum,tag in enumerate(moduleTags):
        n=len(doses)
        scatterTemp=r.TGraph(n)
        scatterTemp.SetMarkerStyle(eNum+2)
        scatterTemp.SetMarkerSize(1)        
        scatterTemp.SetMarkerColor(eNum+1)
        for i in xrange(n):
            x=doses[i]
            y=measurements[doses[i]][tag][parameter]
            scatterTemp.SetPoint(i,x,y)
        #scatterTemp.Draw("AL")
        multiGr.Add(scatterTemp)
        leg.AddEntry(scatterTemp,tag,'P')
    multiGr.Draw("AP")

    multiGr.SetTitle(title);
    multiGr.GetXaxis().SetTitle("Dose [MRad]");
    multiGr.GetYaxis().SetTitle(parameter);
    leg.Draw()
    c1.SaveAs(outputFile)

#parameter  = raw_input('Desired parameter (par0ia,par1ia,par2ia,par0vd,par1vd,par0va,par1va,Vbg): ')
#outputFile = raw_input('Output file name: ')

doses           = [0,2,4,8,17,34]
moduleTags      = ['B1','C1','C2','C3']

p17Measurements = {}    #Dictionary with parameter values for every dose, chipTag and each parameter (for p17 measurements)
m5Measurements  = {}    #structure of the dict is measurements[dose][tag][param], for instance measurements[2]['C1']['Vbg']

#Loads the parameters in the dictionaries
for dose in doses:
    tempDictp17 = {}
    tempDictm5  = {}
    for tag in moduleTags:
        if tag == 'B1':
            m5Path  = '/users/mrogul/Work/Iana/PROC'+tag+'_FulltestROCB'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROCB_m5_1/Dictionary.json'
            p17Path = '/users/mrogul/Work/Iana/PROC'+tag+'_FulltestROCB'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROCB_p17_1/Dictionary.json'
        else:
            m5Path  = '/users/mrogul/Work/Iana/PROC'+tag+'_FulltestROC'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROC_m5_1/Dictionary.json'
            p17Path = '/users/mrogul/Work/Iana/PROC'+tag+'_FulltestROC'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROC_p17_1/Dictionary.json'

        tempDictp17[tag]= readParams(p17Path)
        tempDictm5[tag] = readParams(m5Path)

    p17Measurements[dose] = tempDictp17
    m5Measurements[dose]  = tempDictm5

parameters=['par0ia','par1ia','par2ia','par0vd','par1vd','par0va','par1va','Vbg']

for parameter in parameters:
    multiPlot(p17Measurements,doses,moduleTags,parameter,title=parameter,outputFile='p17'+parameter+'.pdf')
    multiPlot(p17Measurements,doses,moduleTags,parameter,title=parameter,outputFile='m5'+parameter+'.pdf')