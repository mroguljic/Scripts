import json
import numpy
import ROOT as r
from array import array
import sys


def calc_currents(dose,temperature,I_nom=24.):	
#Calculates current using fitted curve and I_nom as the "x"
#fitting params change with dose - we need to provide the dose (in MRad)
#temperature is an integer; since we work with only 17 and -5, use only these values

	if int(temperature)>=0:
		temp_tag='p'
	if int(temperature)<0:
		temp_tag='m'
	print "Calculating Iadc for "+str(dose)+" MRad, at "+temp_tag+str(temperature)+" Celsius and I_ana "+str(I_nom)+" mA\n"
	
	chips=[['B1'],['C1'],['C2'],['C3']]
	currents=[]

	#load fit params
	for chip in chips:
		params=root_params(dose,temp_tag,chip[0])
		chip.append(params)
	
	#chip[i][0] is a chip tag, and chip[i][1] is a list with 3 parameters
	#evaluate current
	for chip in chips:
		current=chip[1][0]+chip[1][1]*I_nom+chip[1][2]*I_nom*I_nom
		currents.append(current)

	print "Chip parameters"
	print chips
	print "Currents (mA)"
	print currents
	print '--------------\n'

	return currents

def json_params(dose,temp,chip):	
#get params from json file - not precise

	if temp=='p':
		temp='p17'
	elif temp=='m':
		temp='m5'
	else:
		print "Invalid temp tag "+temp

	if chip=='B1':
		folderPath='PROC'+chip+'_FulltestROCB'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROCB_'+temp+'_1'
	else:
		folderPath='PROC'+chip+'_FulltestROC'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROC_'+temp+'_1'

	params=[]
	for i in xrange(0,3):

		param_path='/ReadbackParameter_par'+str(i)+'ia/'
		with open(folderPath+param_path+'KeyValueDictPairs.json', 'r') as fp:
			obj   = json.load(fp)
			params.append(float(obj['mu']['Value']))
	
	#print params
	return params

def root_params(dose,temp,chip): 
#get params from root file at said dose (just the number (in MRad)),
#temperature should either be 'p' (for 17C) or 'm' (for -5C)
# and for that chip (B1,C1,C2 or C3)
#more precise than json

	if temp=='p':
		temp='p17'
	elif temp=='m':
		temp='m5'
	else:
		print "Invalid temp "+temp

	if chip=='B1':
		folderPath='PROC'+chip+'_FulltestROCB'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROCB_'+temp+'_1'
	else:
		folderPath='PROC'+chip+'_FulltestROC'+str(dose)+'MRad/QualificationGroup/ModuleFulltestROC_'+temp+'_1'

	params=[]
	for i in xrange(0,3):
		param_path='/ReadbackParameter_par'+str(i)+'ia/'
		rootFile=r.TFile(folderPath+param_path+'ReadbackParameter.root');
		canvas=rootFile.Get("c1")
		graph=r.TH1D(canvas.GetListOfPrimitives().At(1))
		params.append(graph.GetBinContent(1))
		
	#print params
	return params
	
def plot_error_bars(temperature,fileName,doses_plot,means,null_array,stds):
#plots means and error bars of all chips
#temperature, 17 or -5, saves plot under fileName
#doses_plot is a list of doses (x axis) to plot
#means,stds are arrays of mean/std values for the chips, arranged by ascending dose
#null_array is array filled with zeros (we don't have any spread in x direction)
	c1 = r.TCanvas("c1","A Simple Graph Example",200,10,700,500);
	n=len(doses_plot)
	c1.SetGrid();
	gr = r.TGraphErrors(n,doses_plot,means,null_array,stds)
	gr.SetLineColor(2);
	gr.SetLineWidth(4);
	gr.SetMarkerColor(4);
	gr.SetMarkerStyle(21);
	gr.SetTitle("At "+str(temperature)+" C and 24mA");
	gr.GetXaxis().SetTitle("Dose [MRad]");
	gr.GetYaxis().SetTitle("I_adc/I_adc(0 MRad)");
	gr.Draw("AP");	
	c1.SaveAs(fileName)
	c1.Clear()

def scatter_plot(temperature,fileName,doses,normalized_currents):
#instead of means with error bars, plots a scatter plot
#normalized_currents (y) vs dose (x)
	c1 = r.TCanvas("c1","A Simple Graph Example",200,10,700,500);
	gr=r.TGraph(4*len(doses))
	pts_counter=0
	for dose_tag,dose in enumerate(doses):
		for i in xrange(4):
			y=normalized_currents[dose_tag][i]
			x=dose
			gr.SetPoint(pts_counter,x,y)
			pts_counter+=1

	gr.SetMarkerStyle(24);
	gr.Draw('AP')
	c1.SaveAs(fileName)
	c1.Clear()

def plot_separate(temperature,fileName,doses_plot,Cmeans,null_array,Cstds,Bvalues):
#separates C chips from B chip, plots means and error bars for Cs and scatter plot for B chip

	c1 = r.TCanvas("c1","A Simple Graph Example",200,10,700,500);
	n=len(doses_plot)
	c1.SetGrid();
	err_gr = r.TGraphErrors(n,doses_plot,Cmeans,null_array,Cstds)
	err_gr.SetLineColor(2);
	err_gr.SetLineWidth(4);
	err_gr.SetMarkerColor(4);
	err_gr.SetMarkerStyle(21);

	#err_gr.Draw("AP");	

	scatter_gr = r.TGraph(n)
	for i,dose in enumerate(doses):
		y=Bvalues[i]
		x=dose
		scatter_gr.SetPoint(i,x,y)
	scatter_gr.SetMarkerStyle(31)
	#scatter_gr.Draw("AP")

	multiGr = r.TMultiGraph()
	multiGr.Add(err_gr,"P")
	multiGr.Add(scatter_gr,"P")


	multiGr.Draw("AP")

	multiGr.SetTitle("At "+str(temperature)+" C and 24mA");
	multiGr.GetXaxis().SetTitle("Dose [MRad]");
	multiGr.GetYaxis().SetTitle("I_adc/I_adc(0 MRad)");

	leg = r.TLegend(0.1,0.7,0.5,0.9);
   	#leg.SetHeader("Legend");
   	leg.AddEntry(err_gr,"Means and deviations of normalized currents for C chips","P");
   	leg.AddEntry(scatter_gr,"Normalized current for bare module","P");
   	leg.Draw();


	c1.SaveAs(fileName)
	c1.Clear()


if __name__=="__main__":

	temperature=sys.argv[1]	#-5 or 17
	doses=[0,2,4,8,17,34,50]

	print '---------------------------------------------------------------'
	print 'Starting analysis for doses '+str(doses)+' Mrad at '+str(temperature)+' Celsius'
	print '---------------------------------------------------------------'

	doses_plot			= array('d',doses)		#x axis values (MRad)
	means				= array('d')			#y axis values (includes B1 and C chips)
	stds				= array('d')			#y axis errors (includes B1 and C chips)
	null_array          = array('d') 			#we have no errors on x-axis -> null_array for these errors
	normalized_currents = []					#currents at [x] MRad / current at 0 MRad
	referent_currents   = calc_currents(0,temperature) 		#currents at 0 MRad and minus/plus temperature
	full_chips_means    = array('d')			#mean excluding B1 "chip" - might be interesting
	full_chips_stds		= array('d')			#excluding B1 "chip"
	bare_chip_values	= array('d') 			#normalized current for B1 chip ar various doses
	
	for dose in doses:
		normalized_currents_temp=[]							
		currents_at_dose= calc_currents(dose,temperature)	#Iadc at particular dose in [B1,C1,C2,C3] order
		
		for i,current in enumerate(currents_at_dose):
			normalized_currents_temp.append(current/referent_currents[i])

		normalized_currents.append(normalized_currents_temp)
		
		means.append(numpy.mean(normalized_currents_temp))
		stds.append(numpy.std(normalized_currents_temp))
		
		full_chips_means.append(numpy.mean(normalized_currents_temp[1:]))	#exclude first (B1) chip
		full_chips_stds.append(numpy.std(normalized_currents_temp[1:]))
		
		null_array.append(0)
		bare_chip_values.append(normalized_currents_temp[0])

	separateFileName=str(temperature)+"C_separate.pdf"
	fileName=str(temperature)+"C_errorGraph.pdf"
	scatterFileName=str(temperature)+"C_Scatter.pdf"
	plot_separate(temperature,separateFileName,doses_plot,full_chips_means,null_array,full_chips_stds,bare_chip_values)
	plot_error_bars(temperature,fileName,doses_plot,means,null_array,stds)
	scatter_plot(temperature,scatterFileName,doses,normalized_currents)