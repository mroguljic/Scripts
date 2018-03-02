import json

#Given a path to the "FullTest" json file, extracts
#the parameters and returns them in the form of 
#a dictionary


#example: /users/mrogul/Work/Iana/PROCB1_FulltestROCB0MRad/QualificationGroup/ModuleFulltestROCB_m5_1/Dictionary.json

def readParams(jsonFile):
	params={}
	with open(jsonFile, 'r') as fp:
		jsonObj = json.load(fp)
		#Load these parameters
		params["par0ia"] = float(jsonObj["Chips/Chip0/ReadbackCalIana/KeyValueDictPairs.json"]["par0ia"]["Value"])
		params["par1ia"] = float(jsonObj["Chips/Chip0/ReadbackCalIana/KeyValueDictPairs.json"]["par1ia"]["Value"])
		params["par2ia"] = float(jsonObj["Chips/Chip0/ReadbackCalIana/KeyValueDictPairs.json"]["par2ia"]["Value"])
		params["par0vd"] = float(jsonObj["Chips/Chip0/ReadbackCalVdig/KeyValueDictPairs.json"]["par0vd"]["Value"])
		params["par1vd"] = float(jsonObj["Chips/Chip0/ReadbackCalVdig/KeyValueDictPairs.json"]["par1vd"]["Value"])
		params["par0va"] = float(jsonObj["Chips/Chip0/ReadbackCalVana/KeyValueDictPairs.json"]["par0va"]["Value"])
		params["par1va"] = float(jsonObj["Chips/Chip0/ReadbackCalVana/KeyValueDictPairs.json"]["par1va"]["Value"])
		params["Vbg"]    = float(jsonObj["Chips/Chip0/ReadbackCalVbg/KeyValueDictPairs.json"]["Vbg"]["Value"])
	
	return params