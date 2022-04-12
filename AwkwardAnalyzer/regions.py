import awkward1 as ak

def get_mask_Filter(tree_):
    mask_Filter = ( (tree_.Flag_goodVertices ) &
                  (tree_.Flag_globalSuperTightHalo2016Filter) &
                  (tree_.Flag_HBHENoiseFilter) &
                  (tree_.Flag_HBHENoiseIsoFilter) &
                  (tree_.Flag_EcalDeadCellTriggerPrimitiveFilter) &
                  (tree_.Flag_BadPFMuonFilter) 
                  )
    return (mask_Filter)


def get_mask_DYee(tree_):
    mask_DYee = ( (get_mask_Filter(tree_)) &
                  (tree_.OPS_region==3)&
                  (tree_.OPS_2P0F==True)&
                  (tree_.OPS_z_mass>60.)&
                  (tree_.OPS_z_mass<120.)&
                  (tree_.OPS_l1_pt>30.)&
                  (tree_.OPS_l2_pt>20.)&
                  (tree_.OPS_drll>0.3)
              )
    return (mask_DYee)


