import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#import func_simple_ch4_mod_base as ch4mod
#import func_simple_ch4_mod_enh_natemis as ch4mod
import func_simple_ch4_mod_tau_11 as ch4mod
#import func_simple_ch4_mod_tau_82 as ch4mod


#Anthropogenic emissions:

scen_list = ['rcp_hist_85','ceds_v2017_gains_v4',
             'ceds_v2021_gains_v4','ceds_v17_ssp',
             'edgar_v7','ceds_v2021']

#Biomass burning emissions:
em_bb_scen = 'GFEDv41s'

oh_anomaly_list = ['none','OsloCTM3','AerChemMIP','CCMI']

clm_run_list = ['CNTRv5_I2000Clm50BgcCrop_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCru_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max',
                'VISIT-CAO',
                'VISIT-VH',
                'Zhang-MERRA2',
                'Zhang-CRU',
                'none']

clm_anomaly='anom_yr' #none'
clm_scale = True      #False

for scen in scen_list:
    print(scen)
    for oh_anomaly in oh_anomaly_list:
        if oh_anomaly == 'none':
            oh_run_list = ['']
        elif oh_anomaly == 'OsloCTM3':
            oh_run_list = ['aerocom_historical','histO3','histO3_ceds2021']
        elif oh_anomaly == 'AerChemMIP':
            oh_run_list = ['modelmean']
        elif oh_anomaly == 'CCMI':
            oh_run_list = ['modelmean','modelmax','modelmin']    
        else:
            print('oh_anomaly_not_defined, stopping...')
            exit()
        for oh_run in oh_run_list:
            for clm_run in clm_run_list:   
                ch4mod.ch4_mod(scen,em_bb_scen,
                       oh_anomaly,oh_run,
                       clm_run,clm_anomaly,clm_scale)
                

plt.show()
print('Done!')
