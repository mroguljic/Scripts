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
#makes a multigraph param vs dose for requested moduleTags and parameter
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

def calculateADC(measurements,dose,chipTag):
#Returns the ADC value for the corresponding Vbg
#using the fit-formula and the calibration -> ADC=par0vd+2*par1vd*Vbg
    par1vd = measurements[dose][chipTag]['par1vd']  
    par0vd = measurements[dose][chipTag]['par0vd']  
    Vbg    = measurements[dose][chipTag]['Vbg']
    adc    = par0vd + 2*par1vd*Vbg
    return adc


def plotADC(measurements,doses,moduleTags,outputFile):
#Plots ADC value dependence on dose
    r.gROOT.SetBatch(1)
    c1 = r.TCanvas('','',200,10,700,500);
    c1.SetGrid();
    multiGr = r.TMultiGraph()
    leg = r.TLegend(0.7,0.7,0.9,0.9);

    for eNum,tag in enumerate(moduleTags):
        n=len(doses)
        scatterTemp=r.TGraph(n)
        scatterTemp.SetMarkerStyle(eNum+2)
        scatterTemp.SetMarkerSize(1)        
        scatterTemp.SetMarkerColor(eNum+1)
        for i in xrange(n):
            x      = doses[i]
            y      = calculateADC(measurements,doses[i],tag)
            scatterTemp.SetPoint(i,x,y)
        multiGr.Add(scatterTemp)
        leg.AddEntry(scatterTemp,tag,'P')
    multiGr.Draw("AP")

    multiGr.SetTitle('ADC values for Vbg');
    multiGr.GetXaxis().SetTitle("Dose [MRad]");
    multiGr.GetYaxis().SetTitle('ADC = par0vd + 2*par1vd*Vbg');
    leg.Draw()
    c1.SaveAs(outputFile)

def normalizedADC(measurements,doses,moduleTags,outputFile):
#plotting ADC values divided by the ADC value at 0 MRad

    r.gROOT.SetBatch(1)
    c1 = r.TCanvas('','',200,10,700,500);
    c1.SetGrid();
    multiGr = r.TMultiGraph()
    leg = r.TLegend(0.7,0.7,0.9,0.9);

    for eNum,tag in enumerate(moduleTags):
        initialAdc = calculateADC(measurements,0,tag)
        n=len(doses)
        scatterTemp=r.TGraph(n)
        scatterTemp.SetMarkerStyle(eNum+2)
        scatterTemp.SetMarkerSize(1)        
        scatterTemp.SetMarkerColor(eNum+1)
        for i in xrange(n):
            x      = doses[i]
            adc    = calculateADC(measurements,doses[i],tag)
            y      = adc/initialAdc
            scatterTemp.SetPoint(i,x,y)
        multiGr.Add(scatterTemp)
        leg.AddEntry(scatterTemp,tag,'P')
    multiGr.Draw("AP")

    multiGr.SetTitle('ADC[X MRad]/ADC[0 MRad]');
    multiGr.GetXaxis().SetTitle("Dose [MRad]");
    multiGr.GetYaxis().SetTitle('ADC[X]/ADC[0]');
    leg.Draw()
    c1.SaveAs(outputFile)


def VoltageFromADC(measurements,doses,moduleTags,outputFile):
#Inversing the fit formula adcValue=(2)*par1vd*Vbg+par0vd
# -> Voltage=(adcValue-par0vd)/par1vd (*2)
# adcValue is set as adcValue for dose=0 MRad (as calculated in plotADC)

    r.gROOT.SetBatch(1)
    c1 = r.TCanvas('','',200,10,700,500);
    c1.SetGrid();
    multiGr = r.TMultiGraph()
    leg = r.TLegend(0.1,0.7,0.25,0.9);

    for eNum,tag in enumerate(moduleTags):
        adcValue    = calculateADC(measurements,0,tag)
        n           = len(doses)
        scatterTemp = r.TGraph(n)
        scatterTemp.SetMarkerStyle(eNum+2)
        scatterTemp.SetMarkerSize(1)        
        scatterTemp.SetMarkerColor(eNum+1)
        for i in xrange(n):
            x      = doses[i]
            par1vd = measurements[doses[i]][tag]['par1vd']  
            par0vd = measurements[doses[i]][tag]['par0vd']  
            Vbg    = measurements[doses[i]][tag]['Vbg']
            y      = (adcValue-par0vd)/(par1vd*2)
            scatterTemp.SetPoint(i,x,y)
        multiGr.Add(scatterTemp)
        leg.AddEntry(scatterTemp,tag,'P')
    multiGr.Draw("AP")

    multiGr.SetTitle('Voltage calculated using ADC[0 Mrad] in ADC=par0vd+2*par1vd*Vbg');
    multiGr.GetXaxis().SetTitle("Dose [MRad]");
    multiGr.GetYaxis().SetTitle('Voltage');
    leg.Draw()
    c1.SaveAs(outputFile)

def VbgAdcRatioChange(measurements,doses,moduleTags,outputFile):
#Ratio of adc/Vbg ADC values from adcValue=2*par1vd*Vbg+par0vd divided
#by the the same ratio at 0 MRad

    r.gROOT.SetBatch(1)
    c1 = r.TCanvas('','',200,10,700,500);
    c1.SetGrid();
    multiGr = r.TMultiGraph()
    leg = r.TLegend(0.1,0.7,0.25,0.9)

    for eNum,tag in enumerate(moduleTags):
        initialVbg   = measurements[0][tag]['Vbg']
        initialAdc   = calculateADC(measurements,0,tag)
        initialRatio = initialVbg/initialAdc
        n=len(doses)
        scatterTemp = r.TGraph(n)
        scatterTemp.SetMarkerStyle(eNum+2)
        scatterTemp.SetMarkerSize(1)        
        scatterTemp.SetMarkerColor(eNum+1)
        for i in xrange(n):
            x      = doses[i]
            adc    = calculateADC(measurements,doses[i],tag)
            Vbg   = measurements[doses[i]][tag]['Vbg']
            y      = (Vbg/adc)/initialRatio
            scatterTemp.SetPoint(i,x,y)
        multiGr.Add(scatterTemp)
        leg.AddEntry(scatterTemp,tag,'P')
    multiGr.Draw("AP")

    multiGr.SetTitle('Vbg/ADC relative ratio change for different doses');
    multiGr.GetXaxis().SetTitle("Dose [MRad]");
    multiGr.GetYaxis().SetTitle('(Vbg/ADC at X MRad)/(Vbg/ADC at 0 MRad)');
    leg.Draw()
    c1.SaveAs(outputFile)

def VbgRelativeToADC(measurements,doses,moduleTags,outputFile):
#Plots Vbg/(ADC[X]/ADC[0]) vs X (X=Dose in MRad)
    r.gROOT.SetBatch(1)
    c1 = r.TCanvas('','',200,10,700,500);
    c1.SetGrid();
    multiGr = r.TMultiGraph()
    leg = r.TLegend(0.7,0.2,0.9,0.4);

    for eNum,tag in enumerate(moduleTags):
        initialAdc = calculateADC(measurements,0,tag)
        n=len(doses)
        scatterTemp=r.TGraph(n)
        scatterTemp.SetMarkerStyle(eNum+2)
        scatterTemp.SetMarkerSize(1)        
        scatterTemp.SetMarkerColor(eNum+1)
        for i in xrange(n):
            x      = doses[i]
            adc    = calculateADC(measurements,doses[i],tag)
            Vbg    = measurements[doses[i]][tag]['Vbg']
            y      = Vbg/(adc/initialAdc)
            scatterTemp.SetPoint(i,x,y)
        multiGr.Add(scatterTemp)
        leg.AddEntry(scatterTemp,tag,'P')
    multiGr.Draw("AP")

    multiGr.SetTitle('Vbg/(ADC[X MRad]/ADC[0 MRad])');
    multiGr.GetXaxis().SetTitle("Dose [MRad]");
    multiGr.GetYaxis().SetTitle('Vbg/(ADC[X]/ADC[0]) values');
    leg.Draw()
    c1.SaveAs(outputFile)

def loadParameters(doses,moduleTags):
#Loads parameter values for the measurements in two dictionary. First one is for measurements at +17C and the second one at -5C
#Dictionary structure is dict[dose][tag][param], for instance measurements[2]['C1']['Vbg'] returns Vbg for C1 chip at 2MRad irradiation
    p17Measurements = {}
    m5Measurements  = {}

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

    return [p17Measurements, m5Measurements]



doses           = [0,2,4,8,17,34,50]
moduleTags      = ['B1','C1','C2','C3']
measurements    = loadParameters(doses,moduleTags)
p17Measurements = measurements[0]
m5Measurements  = measurements[1]

parameters=['par0ia','par1ia','par2ia','par0vd','par1vd','par0va','par1va','Vbg']
for parameter in parameters:
    multiPlot(p17Measurements,doses,moduleTags,parameter,title=parameter,outputFile='p17'+parameter+'.pdf')
    multiPlot(m5Measurements,doses,moduleTags,parameter,title=parameter,outputFile='m5'+parameter+'.pdf')

plotADC(m5Measurements,doses,moduleTags,'m5AdcValues.pdf')
VoltageFromADC(m5Measurements,doses,moduleTags,'m5VoltageFromAdc.pdf')
VbgAdcRatioChange(m5Measurements,doses,moduleTags,'m5AdcVbgRatio.pdf')
normalizedADC(m5Measurements,doses,moduleTags,'m5NormalizedAdc.pdf')
VbgRelativeToADC(m5Measurements,doses,moduleTags,'m5VbgRelativeToAdc.pdf')