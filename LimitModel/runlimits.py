import os 
import numpy as np 
import sys, optparse,argparse
from LimitHelper import *

usage = "python runlimits.py -c em"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-c", "--category", dest="category", default="em")
args = parser.parse_args()
category = args.category

cat_str = category+"_"+category


mass_points = [200,300,350,400,500,600,700]
coupling    = "rtc01"
template_card = "datacards_ttc_2017/ttc_datacard_2017_SR_"+cat_str+"_template.txt"
dc_tmplate=open(template_card).readlines()


RL  = RunLimits("2017","ttc", category, "asimov") 

print ("self.limitlog: ",RL.limitlog)

counter=0
for imass in mass_points:
    mA = str(imass)
    rtc = coupling.split("rtc")[-1]
    
    parameters = "MA"+str(imass)+"_"+coupling
    card_name = template_card.replace("template",parameters)
    print ("card_name: ", card_name)
    
    fout = open(card_name,'w')
    dc_out =  ([iline.replace("MASSPOINT",str(imass)) for iline in dc_tmplate] )
    fout.writelines(dc_out)
    fout.close()
    
    logname = RL.getLimits(card_name)
    
    mode_ = "a"
    if counter==0: mode_="w"
    param_list=(mA,rtc)
    limitlogfile = RL.LogToLimitList(logname,param_list,mode_)



    counter=counter+1
    
## this is out of the for loop 
RL.TextFileToRootGraphs()
RL.SaveLimitPdf1D()
    
    
    
    