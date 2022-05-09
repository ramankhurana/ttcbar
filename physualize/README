

## physualize: a visualisation package for HEPhysicists


## install the code using: 
git clone git@github.com:ramankhurana/ttcbar.git

cd ttcbar/physualize

Running the code is simple, 
1. prepare the python file, plot_attributes.py and process_attributes.py 
2. plot_attributes.py should have the information about which regions, variables you want to plot. 
3. process_attributes.py should have the cross-section information, color, order, should be visible in stack etc, 
4. once the dictionary are prepared, just the the files, at the end, there is a snippet to write this information into a yaml file. 
5. These yaml files are needed to create and instance of the class plotlib. 
6. To save all the plots just do: 

python 
import plotlib as plib
plib.plotlib("plot_attributes.yaml",  "process_attributes.yaml").SaveAllPlots("stack")


or alternatevely you can do following which essentially does the same thing for now: 
python makeplots.py


For cosmetics, you need to edit the plotlib.py and mainly focus on the function:     def plotStackRoot(self,iregion,ivar)

This function is making the stack and missing following items: 
1. ratio canvas 
2. proper data points as per CMS convention 
3. good color codes for histograms 
4. Legend placing 
5. Latex (Experiment and lumi)
6. X and Y axis label, title size and font type. 
7. X and Y ticks. 
8. X and Y log features 
9. Adding systematics histograms [should be done by providing a list of the nuisances e.g. ["pileup", "btag", "bmistag", "prefiring"], and function should loop over them and add them together and plot on the main and ration canvas. 
10. Anything else? 

Items to be added: 