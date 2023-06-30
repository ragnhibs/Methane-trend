import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#Choose path for plotting:
# Baseline, for Fig. 1 in manuscript.
#results_path = './results_base/'

#Enhance wetland emissions and hence natural emissions by 30 Tg yr.
results_path = './results_enh_natemis/'

#Increase methane lifetime due to OH to 11 -> total lifetime of 9.5
#results_path = './results_tau_11/'

#Decrease methane lifetime due to OH to 8.2 -> total lifetime of 7.3
#results_path = './results_tau_8_2/' 


em_antr_scen_list = ['rcp_hist_85',
                     'ceds_v2021_gains_v4',
                     'ceds_v17_ssp',
                     'edgar_v7',
                     'ceds_v2021']

em_antr_short = {'rcp_hist_85':'RCP',
                 'ceds_v2021_gains_v4':'GAINSv4',
                 'ceds_v17_ssp': 'CEDS-2017',
                 'edgar_v7': 'EDGARv7',
                 'ceds_v2021':'CEDS-2021'}
                 


#Choose if I will plot scaled or unscaled natural methane emissions.
#clm_scaled = '_unscaled' 
clm_scaled = ''

colorlist = ['darkgray','orange','dodgerblue','lightgreen','magenta','green']
colorlist_antr = ['gray','violet','darkblue','indianred','lightblue']

#Plot
plt.rcParams['font.size'] = 12
noOfCols=2
noOfRows=2
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(12,10))

#******************************************************************************
#Only plot anthropogenic trend
new_scen=True
for i,scen in enumerate(em_antr_scen_list):
    #set OH and wetland variability to none.
    oh_run_list = ['none']
    clm_run_list = ['none']
    
    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            trend = results["Trend"]

            if(new_scen):
                trend_all = np.zeros([len(trend.values)])
                trend_all[:] = trend.values
                new_scen  = False
            else:
                trend_all = np.vstack((trend_all,trend.values))#,dtype=trend_all.dtype)

            #Plott anthropogenic trend:
            axes[0,0].plot(year,trend,color=colorlist_antr[i],linewidth=1.0, label=em_antr_short[scen])
           
    max_values = np.amax(trend_all,axis=0)
    min_values = np.amin(trend_all,axis=0)

    
axes[1,1].fill_between(year, min_values, max_values,facecolor='gray',alpha= 0.3,zorder=10,label='Anthropogenic CH4 emissions')        
axes[0,0].fill_between(year, min_values, max_values,facecolor='gray',alpha= 0.2) #,zorder=0)

axes[0,0].set_title('(a) Trend due to anthropogenic emissions',loc='left')

#*********************************************************************************     
#Plott diff from anthropogenic emissions with const OH and natemis:
new_scen=True
em_antr_scen_list =['ceds_v17_ssp']  #Choose one.
for i,scen in enumerate(em_antr_scen_list):
    oh_run_list = ['none']
    clm_run_list = ['none']
    filename = results_path + 'results_'+ scen + '_' + clm_run_list[0] + clm_scaled+'_' + oh_run_list[0] +'.txt'
    results = pd.read_csv(filename, index_col=0)
    year = results.index
    trend_control = results["Trend"]

    oh_run_list = ['OsloCTM3histO3',
                   'OsloCTM3aerocom_historical',
                   'CCMImodelmean',
                   'CCMImodelmin',
                   'CCMImodelmax',
                   'AerChemMIPmodelmean']
    for oh_run in oh_run_list:
        filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
        results = pd.read_csv(filename, index_col=0)
        year = results.index
        
        trend = results["Trend"]-trend_control

        if(new_scen):
            trend_all = np.zeros([len(trend.values)])
            
            trend_all[:] = trend.values
            new_scen  = False
        else:
            trend_all = np.vstack((trend_all,trend.values))#,dtype=trend_all.dtype)
                
                       
    print(trend_all.shape)
    max_values = np.amax(trend_all,axis=0)
    min_values = np.amin(trend_all,axis=0)
        
    axes[0,1].fill_between(year, min_values, max_values,
                           facecolor='darkgreen',alpha= 0.2,
                           label='OsloCTM3/AerChemMIP/CCMI') #,zorder=0)
    axes[0,1].set_title('(b) Effect on trend due to OH',loc='left')
    print('Min values OsloCTM3/AerChemMIP/CCMI')
    print(np.nanmin(min_values))
    
    
    #Add COVID#####################
    oh_run = 'OsloCTM3histO3_ceds2021'
    filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
    results = pd.read_csv(filename, index_col=0)
    year = results.index
            
    trend = results["Trend"]-trend_control
    if (oh_run =='OsloCTM3histO3_ceds2021' and clm_run=='none'):
        axes[0,1].plot(year,trend,color='darkgreen', label='OsloCTM3 CEDS21+COVID')
        print('Increase in OsloCTM3 ceds2021+covid 2019 to 2020')
        print(trend.loc[2020]-trend.loc[2019])
        print('Trend in 2007 OsloCTM3 ceds2021+')
        print(trend.loc[2007])
    #################################            

    axes[0,1].legend(ncol=1, fontsize=10,frameon=False)

    
#************************************************************************    
#Plott diff from anthropogenic emissions for natemis CLM
new_scen=True
em_antr_scen_list =['ceds_v17_ssp']
for i,scen in enumerate(em_antr_scen_list): #Only one scen in the list.
    oh_run_list = ['none']
    clm_run_list = ['none']
    filename = results_path + 'results_'+ scen + '_' + clm_run_list[0] + clm_scaled+'_' + oh_run_list[0] +'.txt'
    results = pd.read_csv(filename, index_col=0)
    year = results.index
    trend_control = results["Trend"]

    oh_run_list = ['none']
    clm_run_list = ['CNTRv5_I2000Clm50BgcCrop_f09_g16_VER2',
                    'CNTRv5_I2000Clm50BgcCropCru_f09_g16_VER2',
                    'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2']
    for oh_run in oh_run_list: #'none'
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            
            trend = results["Trend"]-trend_control

            if(new_scen):
                trend_all = np.zeros([len(trend.values)])
                
                trend_all[:] = trend.values
                new_scen  = False
            else:
                trend_all = np.vstack((trend_all,trend.values))#,dtype=trend_all.dtype)
           
    max_values = np.amax(trend_all,axis=0)
    min_values = np.amin(trend_all,axis=0)
            
    axes[1,0].fill_between(year, min_values, max_values,facecolor='darkblue',alpha= 0.2, label='CLM')

    #Plot parameterrange in CLM:
    new_scen  = True
    clm_run_list = ['CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max',
                    'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min',
                    'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max',
                    'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max']
    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            
            trend = results["Trend"]-trend_control

            if(new_scen):
                trend_all = np.zeros([len(trend.values)])
                
                trend_all[:] = trend.values
                new_scen  = False
            else:
                trend_all = np.vstack((trend_all,trend.values))#,dtype=trend_all.dtype)

    max_values = np.amax(trend_all,axis=0)
    min_values = np.amin(trend_all,axis=0)
            
    axes[1,0].fill_between(year, min_values, max_values,
                           facecolor='royalblue',alpha= 0.2, label='CLM parameter sensitivity') 

    #Add visit results
    new_scen  = True
    clm_run_list = ['VISIT-CAO',
                    'VISIT-VH']
    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            
            trend = results["Trend"]-trend_control

            if(new_scen):
                trend_all = np.zeros([len(trend.values)])
                
                trend_all[:] = trend.values
                new_scen  = False
            else:
                trend_all = np.vstack((trend_all,trend.values))#,dtype=trend_all.dtype)

    max_values = np.amax(trend_all,axis=0)
    min_values = np.amin(trend_all,axis=0)
            
    axes[1,0].fill_between(year, min_values, max_values,facecolor='darkviolet',alpha= 0.2, label='VISIT')



    #Add visit results
    new_scen  = True
    clm_run_list = ['Zhang-MERRA2',
                    'Zhang-CRU']

    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            
            trend = results["Trend"]-trend_control

            if(new_scen):
                trend_all = np.zeros([len(trend.values)])
                
                trend_all[:] = trend.values
                new_scen  = False
            else:
                trend_all = np.vstack((trend_all,trend.values))#,dtype=trend_all.dtype)

    max_values = np.amax(trend_all,axis=0)
    min_values = np.amin(trend_all,axis=0)
            
    axes[1,0].fill_between(year, min_values, max_values,facecolor='darkcyan',alpha= 0.2, label='LPJ_wsl')

    
    axes[1,0].legend(ncol=1, fontsize=10,frameon=False)
    axes[1,0].set_title('(c) Effect on trend due to wetland',loc='left')


#Combine everything
em_antr_scen_list = ['rcp_hist_85',
                     'ceds_v2021_gains_v4',
                     'ceds_v17_ssp',
                     'edgar_v7',
                     'ceds_v2021']

new_scen=True
for i,scen in enumerate(em_antr_scen_list):
    clm_run_list = ['none',
                    'CNTRv5_I2000Clm50BgcCrop_f09_g16_VER2',
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

    oh_run_list = ['none',
                   'OsloCTM3histO3',
                   'OsloCTM3aerocom_historical',
                   'OsloCTM3histO3_ceds2021',
                   'CCMImodelmean',
                   'CCMImodelmin',
                   'CCMImodelmax',
                   'AerChemMIPmodelmean']
  
    for oh_run in oh_run_list:
        for clm_run in clm_run_list:
        
            filename = results_path + 'results_'+ scen + '_' + clm_run + clm_scaled+'_' + oh_run +'.txt'
            results = pd.read_csv(filename, index_col=0)
            year = results.index
            
            trend = results["Trend"]

            if(new_scen):
                trend_all = np.zeros([len(trend.values)])
                
                trend_all[:] = trend.values
                new_scen  = False
            else:
                trend_all = np.vstack((trend_all,trend.values))#,dtype=trend_all.dtype)

                
max_values = np.amax(trend_all,axis=0)
min_values = np.amin(trend_all,axis=0)
            
axes[1,1].fill_between(year, min_values, max_values,facecolor='red',alpha=0.2,label='All factors') #,zorder=0)
axes[1,1].legend(fontsize=10,frameon=False, loc='lower left')
axes[1,1].set_title('(d) Trend all factors',loc='left')

#Concontration trend:
axes[0,0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes[0,0].axhline(y=0.0, color='gray', linestyle='-')
axes[0,1].axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes[0,1].axhline(y=0.0, color='gray', linestyle='-')
axes[1,0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes[1,0].axhline(y=0.0, color='gray', linestyle='-')
axes[1,1].axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes[1,1].axhline(y=0.0, color='gray', linestyle='-')

#### Add methane observed trends to the figure
data_trend = pd.read_csv('INPUT/Atm_conc_trend.csv',
                         delimiter=';',header=1,index_col=0)
                         

data_trend = data_trend.loc[:2020]
print(data_trend)


axes[0,0].plot(data_trend["ann inc"],color='black', linewidth=2.0, label='Observed trend')
#axes[0,0].plot(data_trend["ann inc"]+data_trend["unc"],color='black',linestyle='--',linewidth=0.5)
#axes[0,0].plot(data_trend["ann inc"]-data_trend["unc"],color='black',linestyle='--',linewidth=0.5)
axes[0,1].plot(data_trend["ann inc"],color='black', linewidth=2.0)
#axes[0,1].plot(data_trend["ann inc"]+data_trend["unc"],color='black',linestyle='--',linewidth=0.5)
#axes[0,1].plot(data_trend["ann inc"]-data_trend["unc"],color='black',linestyle='--',linewidth=0.5)
axes[1,0].plot(data_trend["ann inc"],color='black', linewidth=2.0)
#axes[1,0].plot(data_trend["ann inc"]+data_trend["unc"],color='black',linestyle='--',linewidth=0.5)
#axes[1,0].plot(data_trend["ann inc"]-data_trend["unc"],color='black',linestyle='--',linewidth=0.5)
axes[1,1].plot(data_trend["ann inc"],color='black', linewidth=2.0)
#axes[1,1].plot(data_trend["ann inc"]+data_trend["unc"],color='black',linestyle='--',linewidth=0.5)
#axes[1,1].plot(data_trend["ann inc"]-data_trend["unc"],color='black',linestyle='--',linewidth=0.5)

ylabel_text = "Methane trend [ppbv year$^{-1}$]"
ylabel_text = "Methane growth rate [ppbv year$^{-1}$]"
axes[0,0].set_ylabel(ylabel_text)
axes[0,1].set_ylabel(ylabel_text)
axes[1,0].set_ylabel(ylabel_text)
axes[1,1].set_ylabel(ylabel_text)


axes[0,0].set_xlim(left=1970)
axes[0,1].set_xlim(left=1970)
axes[1,0].set_xlim(left=1970)
axes[1,1].set_xlim(left=1970)

axes[0,0].set_ylim([-15,20])
axes[0,1].set_ylim([-15,20])
axes[1,0].set_ylim([-15,20])
axes[1,1].set_ylim([-15,20])

axes[0,0].legend(ncol=2, fontsize=10,frameon=False)

plt.show()
