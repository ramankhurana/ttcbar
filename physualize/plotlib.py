import os 
import sys 

import numpy as np
import matplotlib 
import yaml 
import canvasLib as cnvslib
import ROOT as ROOT 
from ROOT import TH1F, TFile, TLegend, THStack
matplotlib.use("pdf") 
import matplotlib.pyplot as plt 




## https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py
## https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.hist.html#matplotlib.axes.Axes.hist
class plotlib:
    def __init__(self, plot_attributes, 
                 process_attributes,
                 legend_attributes="", 
                 plotType="stack", 
                 makeRatio=False, 
                 saveLog=(False,False),
                 areaNormalize=False  ):
        
        self.plot_attr    = yaml.safe_load(open(plot_attributes)) 
        self.process_attr = yaml.safe_load(open(process_attributes))
        self.legend_attr  = process_attributes
        self.plot_type    = plotType
        self.make_ratio   = makeRatio
        self.save_log     = saveLog
        self.area_norm    = areaNormalize ## to be used when plottype is overlay 
        
        self.regions      = self.plot_attr.keys()
        self.processes    = self.process_attr.keys()
        
        self.maxorder     = max( set( [ self.process_attr[ip]["order"] for ip in self.process_attr.keys() ] ) )
        
        self.lumi         = 60000.
        self.prefix       = "../AwkwardAnalyzer/output/"
        print ("maxorder: ", self.maxorder)        
        print ("plot attributes== ", self.plot_attr)
        print ("process attributes== ", self.process_attr.keys())
        
        
    def setrootfiles(self):
        return 0
    def getrootfiles(self):
        return 0
    def getvariables(self):
        return 0
    def plotSingle(self):
        return 0
        
        
    
    def getxs(self,process):
        return self.process_attr[process]["xs"]

    def gettotalevent(self,process):
        
        f = TFile(self.prefix+self.process_attr[process]["fileN"][0])
        h = f.Get("h_total_mcweight")
        return h.Integral()

        
    def phyHist(self, ax):
        colors_ = ["Red", "Blue"]
        step_error=[]
        for icol in range(len(self.columns_)):
            
            
            ## this is for the stack. 
            h_, bin_, patches_ = ax.hist(self.columns_[icol], bins=self.binning_, range=self.Xrange_, weights=self.weight_[icol], histtype="step", color=colors_[icol] )
            center = (bin_[:-1] + bin_[1:]) / 2
            error_  = np.sqrt(h_) * self.weight_[icol][0]
            s,=ax.step(bin_,np.r_[h_,h_[-1]],where='post', color=colors_[icol], )
            e = ax.errorbar(center, h_, yerr=error_, fmt='none', ecolor=colors_[icol])
            step_error.append((s,e))
            
            '''
            h_, bin_ = np.histogram( self.columns_[icol], bins=self.binning_, range=self.Xrange_, weights=self.weight_[icol])
            center = (bin_[:-1] + bin_[1:]) / 2
            error_  = np.sqrt(h_) * self.weight_[icol][0]
            s,=ax.step(bin_,np.r_[h_,h_[-1]],where='post', color=colors_[icol] )
            e = ax.errorbar(center, h_, yerr=error_, fmt='none', ecolor=colors_[icol])# drawstyle="stepfilled")
            
            step_error.append((s,e))
            '''

        ax.legend(step_error, self.legend_, numpoints=1)
        #ax.legend(self.legend_, numpoints=1)
        
        return ax
        
        
    def plotOverlay(self):
                
        fig, ax = plt.subplots()
        
        print ("inside the plotOverlay() function")
        
        ## weights
        weight_column_ = [np.ones_like(icol) for icol in self.columns_ ]
        if self.areaNormalize_: weight_column_ = [np.ones_like(icol)/len(icol) for icol in self.columns_ ]   
        self.weight_   = weight_column_

        
        ## following line takes care of the overflow and underflow bins
        self.columns_ = [np.clip(icol, float(self.Xrange_[0]), float(self.Xrange_[1]) )  for icol in self.columns_]

        
        '''
        ax.hist( self.columns_, \
                 bins=int(self.binning_),\
                 histtype='step', \
                 weights=weight_column_, \
                 range=self.Xrange_,\
                 label=self.legend_)
        '''
        
        ax = self.phyHist(ax)
        print (self.legend_)
        #ax.legend()
        
        figureTitle = self.experiment_ + " " + self.plotType_
        ax.set_title(figureTitle, x=0.2)
        if len(self.axisTitle_)==2: 
            ax.set_xlabel(self.axisTitle_[0], x=0.88)
            ax.set_ylabel(self.axisTitle_[1])
        
        plt.savefig(self.pdfname_+".pdf")
        return 0
    

    def LegendLib(self):
        leg = TLegend(0.1, 0.70, 0.89, 0.89)
        leg.SetBorderSize(0)
        leg.SetNColumns(2)
        leg.SetLineColor(1)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.04)
        return leg 



    def SaveAllPlots(self,mode="overlay"):
        
        ## these plots will be made for each region. 
        for iregion in self.regions:
            variables = self.plot_attr[iregion].keys()
            for ivar in variables:
                if mode=="overlay": self.plotOverlayRoot(iregion,ivar)
                if mode=="stack": self.plotStackRoot(iregion,ivar)

    def plotOverlayRoot(self,iregion,ivar):
                        
        ## get canvas for each variable 
        canvas = cnvslib.EPCanvas() 
        leg = self.LegendLib()
        
        ## for each variable loop over all the rootfiles
        f = {}
        histList = {}
        
        for iprocess in range(len(self.processes)):
            ip = self.processes[iprocess]
            rootfile = self.process_attr[ip]["fileN"][0] ## taking only the first file from the root file list
            instack  = self.process_attr[ip]["instack"]
            if instack: 
                print ("opening file: ", rootfile)
                f[iprocess]  = TFile(self.prefix+rootfile,"READ")
                print ("file: ../../output/"+rootfile)
                print ("ivar: ", ivar)
                histo = f[iprocess].Get("h_reg_DYee_"+ivar)
                histo.Scale(1./histo.Integral())
                
                ## cosmetics 
                
                histo.GetXaxis().SetTitle(self.plot_attr[iregion][ivar]["xtit"])
                histo.GetYaxis().SetTitle(self.plot_attr[iregion][ivar]["ytit"])
                
                histo.SetLineColor(self.process_attr[ip]["color"])
                histo.SetLineWidth(2)
                
                leg.AddEntry(histo,self.process_attr[ip]["leg"],"PL")
                
                

                print ("integral: ",histo.Integral())
                #histList.append(histo)
                if iprocess==0:
                    histo.Draw()
                if iprocess>0:
                    histo.Draw("same")
        leg.Draw()
        canvas.SaveAs("plots/h_"+ivar+".pdf")
                

                
        ## draw histogram if addstack is true 
        #self.plot_attr[iregion][ivar]
        
                
        


    def plotStackRoot(self,iregion,ivar):
        #maxorder = max( set( [ a[ip]["order"] for ip in a.keys() ] ) )
        
        ## get canvas for each variable 
        thstack = THStack ("THStack","THStack")
        
        canvas = cnvslib.EPCanvas() 
        leg = self.LegendLib()
        
        ## for each variable loop over all the rootfiles
        f = {}
        histList = {}
        for io in range(self.maxorder):
            for iprocess in range(len(self.processes)):
                ip = self.processes[iprocess]
                #print ("order: ", self.process_attr[ip]["order"])
                if io == self.process_attr[ip]["order"] :
                    print ("total event: ",self.gettotalevent(ip))
                    print ("cross-section: ", self.getxs(ip))
                    
                                 
                    rootfile = self.process_attr[ip]["fileN"][0] ## taking only the first file from the root file list
                    instack  = self.process_attr[ip]["instack"]
                    if instack: 
                        print ("opening file: ", rootfile)
                        f[iprocess]  = TFile(self.prefix+rootfile,"READ")
                        print ("file: ../../output/"+rootfile)
                        print ("ivar: ", ivar)
                        histo = f[iprocess].Get("h_reg_DYee_"+ivar)
                        histo.Scale(1./histo.Integral())
                        
                        ## cosmetics 
                        
                        histo.GetXaxis().SetTitle(self.plot_attr[iregion][ivar]["xtit"])
                        histo.GetYaxis().SetTitle(self.plot_attr[iregion][ivar]["ytit"])
                        
                        histo.SetLineColor(self.process_attr[ip]["color"])
                        histo.SetLineWidth(2)
                        
                        thstack.Add(histo)
                        leg.AddEntry(histo,self.process_attr[ip]["leg"],"PL")
                        
                        
                        
                        print ("integral: ",histo.Integral())
                        #histList.append(histo)
                        #if iprocess==0:
                        #    histo.Draw()
                        #if iprocess>0:
                        #    histo.Draw("same")
        thstack.Draw()
        leg.Draw()
        canvas.SaveAs("plots/hstack_"+ivar+".pdf")

        return 0
    def plotEfficiency(self):
        return 0
    def plotEfficiencyOverlay(self):
        return 0
    def plot1DLimits(self):
        return 0
    def plotLimitsOverlay(self):
        return 0
    def plot2dLimits(self):
        return 0
        
