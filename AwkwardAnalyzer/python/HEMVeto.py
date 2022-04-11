## Module to check if one of the jet is in the HEM region and the event needs to be veto for analysis 
## Raman Khurana: 08-04-2022 
## V0: basic implementation, loops over the jets to find if one of the jet is in the HEM region and return a flag which can be used in the analysis 
## I will try to add the fast version in the next iteration.  


import numpy as np 


## start of HEM issue 

def isinhemregion(run, jeteta, jetphi):
    isinHEMRegion = False 
    if run >= 319077: 
        if ((-3.2 < jeteta) & (jeteta<-1.3)) & ((-1.57<jetphi) & (jetphi< -0.87)): 
            isinHEMRegion = True 
    return isinHEMRegion





## for testing purpose 
##fabricated jeteta and phi and run number 
def main ():
    jeteta = [-3.11, 1.5,2.9]
    jetphi = [-0.90, 1.2, 3.0]
    run = 319177
    
    hemveto=[]
    for ijet in range(len(jeteta)): 
        hemveto.append(isinhemregion(run, jeteta[ijet], jetphi[ijet]))
    veto =  (np.sum(np.array(hemveto))) >=1 
    print ("veto; ", veto)

    
        

main()

        
        
