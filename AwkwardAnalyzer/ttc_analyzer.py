import sys, numpy, math, time, copy
start = time.clock()
import uproot4
import awkward1 as ak
from ROOT import TFile, TH1F
import multiprocessing as mp
sys.path.append('python/')
from utils import getpt, geteta, getphi, getrecoil, DeltaPhi, getMT, getRecoilPhi, getrecoil1, getN, VarToHist, SetHist, FileToList, deltaR
from functools import partial
from regions import get_mask_DYee

inputfile=sys.argv[1]
outputfile="output/"+sys.argv[2]
rootfilename=sys.argv[2]
inputfileList=inputfile+rootfilename
print ("running the code for: ", inputfileList)

def Isdata():
    isdata=False
    if ("DoubleMuon" in rootfilename) | ("EGamma" in rootfilename) |  ("MuonEG" in rootfilename) | ("MET" in rootfilename) |  ("DoubleMuon" in rootfilename) | ("SingleMuon" in rootfilename) : 
        isdata=True
    print ("isdata : ", isdata)
    return isdata
    
def GetRegion(out_events, region):
    thisregion = out_events[(out_events[region]==True)]
    thisregion_ = thisregion[~(ak.is_none(thisregion))]
    return thisregion_

def GetEntries(out_events, region):
    thisregion_ = GetRegion(out_events, region)
    return len(thisregion_)
    
def runOneFile(filename):
    end = time.clock()
    print ("before reading the arrays:  %.4gs" % (end-start))
    mycache = uproot4.LRUArrayCache("500 MB")
    file_=uproot4.open(inputfileList)
    nevents = 0.0
    if Isdata()==False:  
        print ("getting the events for normalisation", ak.to_list(file_["nEventsGenWeighted"].values())[1])
        nevents=ak.to_list(file_["nEventsGenWeighted"].values())[1]
    fulltree_=ak.ArrayBuilder() ## defauter, to merge the zip later for each chunch of rootfile. 
    niterations=0
    
    allvars=[]
    ## which variables to read. 
    allvars=['OPS_region', 'OPS_2P0F', 'OPS_drll', 'OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l2_pt','OPS_l2_eta',
             'OPS_l2_phi','OPS_z_pt','OPS_z_eta','OPS_z_phi', 'OPS_z_mass',
             'Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 
             'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter', 
             'Flag_eeBadScFilter', 'Flag_ecalBadCalibFilter', 
             'nHad_tau', 'n_tight_jet']
    if not Isdata():
        allvars.append('puWeight')  ## for MC add PU weight, more will arrive here. 
    
    for tree_ in uproot4.iterate(file_["Events"],allvars,
                                 step_size=100000):
        niterations=niterations+1
        print ("iteration number: ", niterations)
        ## dict of name in tuples and local name, right now they are kept exactly the same. 
        allvars_dict = {}
        for ivar in allvars:
            allvars_dict[ivar] = tree_[ivar]
            
        maintree_ = ak.zip(allvars_dict, 
                           depth_limit=1
                       )
        
        maintree_["DYee"] = get_mask_DYee(maintree_) ## name of new columns should be same as in the plot_attributes.py 
        maintree_["weight_DYee"]= 1 ## default value for data 
        if not Isdata: maintree_["weight_DYee"]=maintree_["puWeight"]
        
        ## concatename the awkward arrary from each chunck, and use the fulltree_ outside this loop, for plotting and other purposes. 
        fulltree_=ak.concatenate([maintree_,fulltree_],axis=0)
        
    print ("NOW ENTERING THE HISTOGRAMMING")
    from plot_attributes import attributes 
    regions = attributes.keys()
    
    f = TFile(outputfile,"RECREATE")
    for ireg in regions:
        thisregion  = fulltree_[fulltree_[ireg]==True]
        thisregion_ = thisregion[~(ak.is_none(thisregion))]
        weight_ = "weight_"+ireg
        
        variables = attributes[ireg].keys()
        for ivar in variables:
            binning = attributes[ireg][ivar]["bin"]
            hist_name_ = "h_reg_"+ireg+"_"+ivar
            h = VarToHist(thisregion_[ivar], thisregion_[weight_], hist_name_, binning)
            f.cd()
            h.Write()
    

    f.cd()
    h_total  = TH1F("h_total_mcweight", "h_total_mcweight", 2,0,2)
    
    h_total.SetBinContent(1,nevents)
    h_total.Write()

runOneFile(inputfileList)
final= time.clock()
print ("total time =  %.4gs" % (final-start))




### OLD BUT GOLD 

##setup for one object in one zip         
##''' 
##jets = ak.zip({ "Jet_eta":tree_["Jet_eta"], 
##                "Jet_phi":tree_["Jet_phi"], 
##                "Jet_pt":tree_["Jet_pt"]
##            },
##              depth_limit=1)
##
##
##
##electrons = ak.zip({"Electron_eta":tree_["Electron_eta"],
##                    "Electron_mass":tree_["Electron_mass"],
##                    "Electron_pt":tree_["Electron_pt"],
##                    "Electron_phi":tree_["Electron_phi"]   
##                },
##                   depth_limit=1)
##
##
##
##cms_events = ak.zip({"jets":jets,"electrons":electrons})
##print (ak.to_list(cms_events["jets"].Jet_pt[:10]))
##jets["njets"] = ak.sum(jets["Jet_pt"]>100,axis=-1)
##print ("numnber of jets", jets.njets[:10])
##jetele = electrons[(jets.njets>0)]
##print ("jet ele: ", ak.to_list(jetele[:10]))
##'''


    
