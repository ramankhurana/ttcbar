## Module to check if one of the jet is in the HEM region and the event needs to be veto for analysis 
## Raman Khurana: 08-04-2022 
## V0: basic implementation, loops over the jets to find if one of the jet is in the HEM region and return a flag which can be used in the analysis 
## I will try to add the fast version in the next iteration.  


import numpy as np 
np.random.seed(12345)


## start of HEM issue 

def isinhemregionData(run, jeteta, jetphi):
    isinHEMRegion = False 
    if run >= 319077: 
        if ((-3.2 < jeteta) & (jeteta<-1.3)) & ((-1.57<jetphi) & (jetphi< -0.87)): 
            isinHEMRegion = True 
    return isinHEMRegion


def isinhemregionMC(run, jeteta, jetphi):
    isinHEMRegion = False 
    rndmn = np.random.uniform()
    frac = 0.66  
    print ("random number: ",rndmn)
    if rndmn>frac:
        if ((-3.2 < jeteta) & (jeteta<-1.3)) & ((-1.57<jetphi) & (jetphi< -0.87)): 
            isinHEMRegion = True 
    return isinHEMRegion



def isinhemregion(run, jeteta, jetphi, isdata):
    veto_ = False
    if isdata:
        veto_ = isinhemregionData(run, jeteta, jetphi)
    if not isdata:
        veto_ = isinhemregionMC(run, jeteta, jetphi)

## for testing purpose 
##fabricated jeteta and phi and run number 
def main ():
    jeteta = [-3.21, 1.5,2.9]
    jetphi = [-0.90, 1.2, 3.0]
    run = 319177
    
    hemveto=[]
    for ijet in range(len(jeteta)): 
        hemveto.append(isinhemregionMC(run, jeteta[ijet], jetphi[ijet]))
    veto =  (np.sum(np.array(hemveto))) >=1 
    print ("veto; ", veto)

    
        

main()

        
        
