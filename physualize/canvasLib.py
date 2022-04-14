from ROOT import TCanvas, gStyle, gROOT

def style_():
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    gROOT.SetBatch(1)


def EPCanvas(logy=0, logx=0, lm=0.12, rm=0.06, tm=0.10, bm=0.11 ):
    
    style_()
    c = TCanvas("c","c",800, 800)
    
    c.SetTicks()
    
    c.SetLogy(logy)
    c.SetLogx(logx)
    
    c.SetLeftMargin(lm)
    c.SetRightMargin(rm)
    c.SetTopMargin(tm)
    c.SetBottomMargin(bm)
    gStyle.SetOptStat(0);

    return c


def EPCanvas2DLongXColz(logy=0, logx=0, lm=0.12, rm=0.16, tm=0.10, bm=0.11 ):
    style_()
    
    c = TCanvas("c","c",1000, 800)
    
    c.SetTicks()
    
    c.SetLogy(logy)
    c.SetLogx(logx)
    
    c.SetLeftMargin(lm)
    c.SetRightMargin(rm)
    c.SetTopMargin(tm)
    c.SetBottomMargin(bm)
    
    return c
    
def EPCanvasRatio(logy=0, logx=0, lm=0.12, rm=0.06, tm=0.10, bm=0.11):
    style_()
    ## modify it as per needs 
    c = TCanvas("c","c",800, 800)
    
    c.SetTicks()
    
    c.SetLogy(logy)
    c.SetLogx(logx)
    
    c.SetLeftMargin(lm)
    c.SetRightMargin(rm)
    c.SetTopMargin(tm)
    c.SetBottomMargin(bm)
    
    return c
    







