import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

results_path = './results_base/'
runtype = ''

#results_path = './results_enh_natemis/'
#runtype = '_enh_natemis'

metafile = results_path + 'metadata_rcp_hist_85_none_none.txt'
ant_scen_list = ['rcp_hist_85',
                 'ceds_v2021_gains_v4',
                 'ceds_v17_ssp',
                 'edgar_v7',
                 'ceds_v2021']

em_antr_short = {'rcp_hist_85':'RCP',
                 'ceds_v2021_gains_v4':'GAINSv4',
                 'ceds_v17_ssp': 'CEDS-2017',
                 'edgar_v7': 'EDGARv7',
                 'ceds_v2021':'CEDS-2021'}
colorlist_antr = ['gray','violet','darkblue','indianred','lightblue']


noOfCols=2
noOfRows=2
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(13,10))

oh_run_list = ['none']
clm_run_list = ['none']
clm_scaled = ''
for sc,scen in enumerate(ant_scen_list):    
    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            totemis = results["Antr+BB"]

            print(results)
        
            

            #Emissions:
            axes[0,0].plot(totemis,label=em_antr_short[scen],color=colorlist_antr[sc])
axes[0,0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
        
axes[0,0].set_title('(a) Anthropogenic + Biomass Burning emissions',loc='left')
axes[0,0].set_ylabel("Tg yr$^{-1}$")
axes[0,0].set_ylim([0,500]) 
axes[0,0].legend(loc='lower right')


clm_scaled = ''
ant_scen_list = ['rcp_hist_85']
oh_run_list = ['none']       
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
                'Zhang-CRU']

clm_run_short = {'CNTRv5_I2000Clm50BgcCrop_f09_g16_VER2':'CLM GSWP3',
                 'CNTRv5_I2000Clm50BgcCropCru_f09_g16_VER2':'CLM CRUNCEP',
                 'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2':'CLM CRUJRA',
                 'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max':'CLM CRUJRA fch4max',
                 'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min':'CLM CRUJRA q10ch4min',
                 'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max':'CLM CRUJRA q10ch4max',
                 'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max':'CLM CRUJRA fch4max_q10ch4max',
                 'VISIT-CAO':'VISIT-CAO',
                 'VISIT-VH':'VISIT-VH',
                 'Zhang-MERRA2':'LPJ_wsl-MERRA2',
                 'Zhang-CRU':'LPJ_wsl-CRU'}

init_natemis_output = True

for scen in ant_scen_list:    
    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            totemis = results["natemis"]

            print(results)
        
            if(init_natemis_output):
                totemis.name = clm_run_short[clm_run]
                natemis_output = totemis
                init_natemis_output=False
            else:
                totemis.name = clm_run_short[clm_run]
                natemis_output = pd.concat([natemis_output,totemis],axis=1)

            #Emissions:
            axes[0,1].plot(totemis,label=clm_run_short[clm_run])

            


axes[0,1].set_title('(b) Natural emissions',loc='left')
axes[0,1].set_ylabel("Tg yr$^{-1}$")
axes[0,1].set_ylim([0,300]) 
axes[0,1].legend(ncol=2,loc='lower left',fontsize=8)




oh_anomaly_list = ['OsloCTM3','AerChemMIP','CCMI']
clm_scaled = ''
ant_scen_list = ['rcp_hist_85']
clm_run_list = ['none']
init_oh_output = True
for scen in ant_scen_list:    
    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
            for oh_anomaly in oh_anomaly_list:
                if oh_anomaly == 'none':
                    oh_run_list = ['']
                elif oh_anomaly == 'OsloCTM3':
                    oh_run_list = ['aerocom_historical','histO3','histO3_ceds2021']
                    oh_run_list_out = ['CEDS17 variable met','CEDS17 fixed met','CEDS21+COVID']
                elif oh_anomaly == 'AerChemMIP':
                    oh_run_list = ['modelmean']
                    oh_run_list_out =oh_run_list 
                elif oh_anomaly == 'CCMI':
                    oh_run_list = ['modelmean','modelmax','modelmin']
                    oh_run_list_out =oh_run_list 
#                
                else:
                    print('oh_anomaly_not_defined, stopping...')
                    exit()
                for oh,oh_run in enumerate(oh_run_list):
                    filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_anomaly + oh_run +'.txt'
                    results = pd.read_csv(filename, index_col=0)
                    year = results.index
                    ohfact = results["ch4lifetime_fact"]

                    if(init_oh_output):
                        ohfact.name = oh_anomaly + oh_run_list_out[oh]
                        oh_output = ohfact
                        init_oh_output=False
                    else:
                        ohfact.name = oh_anomaly + oh_run
                        oh_output = pd.concat([oh_output,ohfact],axis=1)
                
                    print(ohfact)
                    
                    #oh_scen =  oh_anomaly + oh_run
                    #df_oh = ohfact
                    
                    
                    axes[1,0].plot(ohfact,label=oh_anomaly  + ' ' +oh_run_list_out[oh])#oh_run)

        
axes[1,0].axvspan(2000, 2007, alpha=0.2, color='lightgray')




axes[1,0].set_title('(c) CH4 lifetime scaling factor',loc='left')
axes[1,0].set_ylabel("scale factor")
axes[1,0].set_ylim([0.95,1.15]) 
axes[1,0].legend(fontsize=8)


df_meta = pd.read_csv(metafile, index_col=0)
df_meta = df_meta.drop(['em_antr_scen','oh_anomaly','clm_run','oh_run','filename_oh','clm_anomaly','em_bb_scen'],axis=1)
bbox=[0.2, 0, 0.9, 1]
axes[1,1].axis('off')
mpl_table = axes[1,1].table(cellText = df_meta.T.values, rowLabels = df_meta.columns, bbox=bbox, colLabels=df_meta.index)



print(oh_output)
#oh_output.to_csv('csv_output/ch4_lifetime_oh_scaling_factors'+runtype+'.csv')
#natemis_output.to_csv('csv_output/natemis'+runtype+'.csv')

plt.show()
