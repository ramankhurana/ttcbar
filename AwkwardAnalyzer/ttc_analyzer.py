import sys
import uproot4
import awkward1 as ak
import numpy
import math
import time
start = time.clock()
from ROOT import TFile, TH1F
import copy
import multiprocessing as mp
from utils import getpt, geteta, getphi, getrecoil, DeltaPhi, getMT, getRecoilPhi, getrecoil1, getN, VarToHist, SetHist, FileToList, deltaR
from functools import partial
inputfile=sys.argv[1]
outputfile=sys.argv[2]

inputfileList=inputfile+"/TTTo1L.root:Events"


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
    fulltree_=ak.ArrayBuilder()
    niterations=0

    allvars=["Jet_eta","Jet_mass","Jet_phi","Jet_pt", "Electron_eta", "Electron_mass", "Electron_phi", "Electron_pt"]
    for tree_ in uproot4.iterate(inputfileList,allvars,
                                 step_size=50000):
        niterations=niterations+1
        jets = ak.zip({ "Jet_eta":tree_["Jet_eta"], 
                        "Jet_phi":tree_["Jet_phi"], 
                        "Jet_pt":tree_["Jet_pt"]
                    },
                      depth_limit=1)
        
        
        
        electrons = ak.zip({"Electron_eta":tree_["Electron_eta"],
                            "Electron_mass":tree_["Electron_mass"],
                            "Electron_pt":tree_["Electron_pt"],
                            "Electron_phi":tree_["Electron_phi"]   
                        },
                           depth_limit=1)
        
        
        cms_events = ak.zip({"jets":jets,"electrons":electrons})
        print (ak.to_list(cms_events["jets"].Jet_pt[:10]))
        jets["njets"] = ak.sum(jets["Jet_pt"]>100,axis=-1)
        print ("numnber of jets", jets.njets[:10])
        jetele = electrons[(jets.njets>0)]
        print ("jet ele: ", ak.to_list(jetele[:10]))
        
        
        
        
                


runOneFile(inputfileList)
