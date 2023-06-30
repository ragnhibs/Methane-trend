import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
Baseline simulation
'''
#func_simple_ch4_mod_base
def ch4_mod(em_antr_scen,em_bb_scen,oh_anomaly,oh_run,
                           clm_run,clm_anomaly,clm_scale):
    print(em_antr_scen+em_bb_scen)

    #Plot the results from the first run, and exit
    plotteval =False 
        
    path_results = './results_base/'
    #Start year and end year for the simulations
    startyr = 1950
    endyear = 2020

    #Scale the emissions to be 149 Tg over the mean period
    #Based on GMB 2020, bottom up.
    wet_emis = 149.0 
    #Natural emissions (including other sources than wetland.)
    em_nat = 215 #  %Methane

    TAU_1 = 9.6
    TAU_2 = 120 #(Stevenson2013 used this)
    TAU_3 = 160 #(Stevenson2013 used this)

    #'Total lifetime used')
    #(1/(1/TAU_1 + 1/TAU_2 + 1/TAU_3))

    #Factor converting emissions to mixing ratios (Tg CH4/ppbv)
    BETA_CH4 = 2.84 
    #Molecular weight CH4: 16.04 g/mol
    #Mass of atmosphere Ma: 5.1352e18 kg (fra Fair)
    #reference to DOI: https://doi.org/10.1175/JCLI-3299.1
    #Molecular weight of air: 28.97 g/mol
    Ma = 5.1352e9*16.04/28.97*1e-9
    #print('Check:')
    #print(BETA_CH4)
    #print(Ma)
        
    #*********************READ INPUTDATA*************************

    #************Read atmospheric concentrations*********************
    #Use the concentrations up to year 1984 from CMIP6 Malte
    #Meinshausen, M., Vogel, E., Nauels, A., Lorbacher, K., Meinshausen,
    #N., Etheridge, D. M., Fraser, P. J., Montzka, S. A., Rayner, P. J.,
    #Trudinger, C. M., Krummel, P. B., Beyerle, U., Canadell, J. G., Daniel,
    #J. S., Enting, I. G., Law, R. M., Lunder, C. R., O'Doherty, S.,
    #Prinn, R. G., Reimann, S., Rubino, M., Velders, G. J. M., Vollmer,
    #M. K., Wang, R. H. J., and Weiss, R.: Historical greenhouse gas
    #concentrations for climate modelling (CMIP6), Geosci. Model Dev.,
    #10,2057-2116, 10.5194/gmd-10-2057-2017, 2017.
    #Use trend:
    #https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/ch4/ch4_gr_gl.txt
    #For the following years.

    path = '/div/qbo/users/ragnhibs/Methane/INPUT/'
    filename = 'ch4_atm_cmip6_upd.txt' #Atmospheric_concentration.csv'
    data_conc = pd.read_csv(path+filename,index_col=0)
    data_conc.index.name = 'Year'
    data_conc.columns = ['CH4']
    
    #Prepare concentration:
    conc_ch4 = data_conc.copy()
    conc_ch4.loc[startyr:endyear]=-1
    
    #************Read anthropogenic emissions*********************
    
    path = '../figures/INPUT/'
    filename = 'anthropogenic_emissions_v2_gfed.txt'
    data_emis = pd.read_csv(path+filename,delimiter=',',index_col=0)
    #Antropogenic emissions:
    emis_antr = data_emis[em_antr_scen].loc[startyr:endyear]
    #Biomass burning emissions:
    emis_bb = data_emis[em_bb_scen].loc[startyr:endyear]

    #Total antropogenic emissions + biomass burning emissions:
    emission_ch4 = (emis_antr + emis_bb) 
    emission_ch4.columns='Antr+BB'
  
    year = emission_ch4.index.values
    antyr = year.size

    df_emissions_ch4 = pd.DataFrame(data=
                                    {'Antr+BB':emission_ch4.values},index=year)
    
    #************Read natural emission perturbation *********************
    #Choose anomaly period
    yr_start_clm = 2000
    yr_end_clm = 2007
    
    first_yr_clm = 1990

    natemis = np.zeros(antyr)
    natemis[:] = em_nat
    df_natemis = pd.DataFrame( {"natemis": natemis},index=year)

    
    if (clm_anomaly != 'none'):
        if(clm_anomaly == 'anom_yr'):
            if (clm_run != 'none'):
                #filename_clm = '/div/amoc/ragnhibs/ICOS/Python/ASCII/annual_totCH4_for_box_model_' + clm_run + '.txt'
                filename_clm = '../figures/ASCII/annual_totCH4_for_box_model_' + clm_run + '.txt'
                print(filename_clm)
                data_clm = pd.read_csv(filename_clm,delimiter=',',index_col=0)
                data_emis.index.name = 'Year'
                #print(data_clm)
                #print(df_natemis)
                
                #Anomaly period:
                mean_val_clm = data_clm.loc[yr_start_clm:yr_end_clm].mean()
                #print(mean_val_clm)
                if(clm_scale):
                    scale_factor =wet_emis/mean_val_clm['Annual']
                else:
                    scale_factor = 1.0
                
                anomalies_clm = data_clm - mean_val_clm
                for yr in data_clm.index:
                    #print(yr)
                    df_natemis["natemis"].loc[yr] = df_natemis["natemis"].loc[yr]  + anomalies_clm['Annual'].loc[yr]*scale_factor
        else:
            print('Not in use')
            print(clm_anomaly)
            exit()
                    
        
#********Read and prepare OH anomalies******************************
    
    if (oh_anomaly !='none'):
        const_oh = 0
    else:
        const_oh = 1

    #Prepare OH-anomalies
    filename_oh =''
    lifetime_fact = np.ones(antyr)
    
    ch4lifetime_fact = pd.DataFrame( {"lifetime_fact": lifetime_fact},index=year)
        
    if (oh_anomaly != 'none'):
        #Ref year for anomaly:
        anom_year = 2000
    
        if(oh_anomaly == 'CCMI'):
            path = '/div/qbo/users/ragnhibs/Methane/OH/DataFromOthers/ForBoxModel/'
            filename_oh = oh_anomaly + '_' + oh_run + '_OH.txt'
            lifetime = pd.read_csv(path+filename_oh,delimiter=',',index_col=0)
            lifetime = lifetime.loc[startyr:endyear]
            lifetime_frac_inv = 1+(1-lifetime)
                        
            lifetime_ref=lifetime_frac_inv.loc[anom_year]
            ch4lifetime_fact.loc[lifetime.index]= lifetime_frac_inv/lifetime_ref

            #Set constant values from end year to end of simulation
            endyr = lifetime.index[-1]
            valend = ch4lifetime_fact.loc[endyr].values
            ch4lifetime_fact.loc[(lifetime.index[-1]+1):endyear]=valend[0]
            
        if(oh_anomaly == 'AerChemMIP'):
            path = '/div/qbo/users/ragnhibs/Methane/OH/DataFromOthers/ForBoxModel/'
            filename_oh = oh_anomaly + '_' + oh_run + '_OH.txt'
            lifetime = pd.read_csv(path+filename_oh,delimiter=',',index_col=0)
            lifetime = lifetime.loc[startyr:endyear]
            lifetime_frac_inv = 1+(1-lifetime)
            #Already reference year 2000?
            ch4lifetime_fact.loc[lifetime.index]=lifetime_frac_inv

            #Set constant values from end year to end of simulation
            endyr = lifetime.index[-1]
            valend = ch4lifetime_fact.loc[endyr].values
            ch4lifetime_fact.loc[(lifetime.index[-1]+1):endyear]=valend[0]
            
        if(oh_anomaly == 'OsloCTM3'):
            path = '/div/qbo/users/ragnhibs/Methane/OH/OsloCTM3/ForBoxModel/'
            filename_oh = oh_anomaly + '_CH4lifetime_' + oh_run +'.txt'
            lifetime = pd.read_csv(path+filename_oh,delimiter=',',index_col=0)
            lifetime = lifetime.loc[startyr:endyear]

            lifetime_ref = lifetime['Lifetime'].loc[anom_year]
            ch4lifetime_fact.loc[lifetime.index]=lifetime/lifetime_ref

           
    
    #END READING INPUT DATA
    #*********************************            
    #Concentration at start of simulations
    conc_pre = conc_ch4.loc[startyr-1].values
   
    #Number of iteration per year
    IDTM=12 #12 #24
    XC = np.zeros(IDTM+1) #IDTM+1 entries.
    #print(XC)

    print('Start calculations... ')
    for i in range(0,antyr):
        #print(year[i])

        em_nat_ch4 = np.zeros(12)
        if(clm_anomaly == 'anom_yr'):
            em_nat_ch4[:] = df_natemis["natemis"].loc[year[i]]
        elif (clm_anomaly == 'anom_month'):
            em_nat_ch4[:] =  df_natemis_mnd.loc[year[i]]
            print(em_nat_ch4)
            
        else:
            em_nat_ch4[:] = df_natemis["natemis"].loc[year[i]]

        #print(em_nat_ch4)
        #exit()
        
        XC[0] = conc_pre

        if const_oh == 1:
            q = 1.0/TAU_1
        else:
            q = 1.0/(TAU_1*ch4lifetime_fact.loc[year[i]])

        
        q = q + 1/TAU_2 + 1/TAU_3
        # Divide q by time
        q=q/IDTM;

        for t in range(0,IDTM):
            em = df_emissions_ch4["Antr+BB"].loc[year[i]] 
            em = em + em_nat_ch4[t]
            
            ach = XC[t]
            em = em/IDTM
            
            pc = em/BETA_CH4;
            ach = pc/q+(ach-pc/q)*np.exp(-q*1.0);      
            XC[t+1] = ach;
                
        #Start next years calculations with this value
        conc_pre = XC[t+1]
        
        conc_ch4.loc[year[i]]= XC[IDTM]
        #print(t+1)
        #print(IDTM)
        #exit()
        #conc_ch4.loc[year[i]]= np.mean(XC)         


    #Write results to file:
    filename_out_meta = path_results + '/metadata_'+ em_antr_scen + '_' + clm_run +'_' + oh_anomaly + oh_run +'.txt'
    meta_data = {'startyr': startyr, 
                 'endyear': endyear, 
                 'TAU_1': TAU_1,
                 'TAU_2': TAU_2,
                 'TAU_3': TAU_3,
                 'BETA_CH4': BETA_CH4,
                 'em_nat': em_nat,
                 'em_antr_scen': em_antr_scen,
                 'em_bb_scen': em_bb_scen,
                 'oh_anomaly': oh_anomaly, 
                 'clm_run': clm_run,
                 'clm_anomaly': clm_anomaly,
                 'wet_emis': wet_emis,
                 'oh_run': oh_run,
                 'filename_oh': filename_oh}
    
    df_meta = pd.DataFrame(data=meta_data, index=['Value'])
    #print(df_meta)
    df_meta.to_csv(filename_out_meta)
    #Calculate model trend
    model_trend = np.zeros(antyr)
    
    for yr in year:
        if (yr == startyr):
            model_trend[yr-startyr] = np.nan
        else:
            model_trend[yr-startyr] = conc_ch4.loc[yr] - conc_ch4.loc[yr-1]
                
    totemis = df_natemis["natemis"].values + df_emissions_ch4["Antr+BB"].values
    results={"natemis":df_natemis["natemis"].values,
             "Antr+BB":df_emissions_ch4["Antr+BB"].values,
             "Totemis":totemis,
             "ch4lifetime_fact":ch4lifetime_fact['lifetime_fact'].values,
             "Conc":conc_ch4['CH4'].loc[startyr:endyear].values,
             "Trend": model_trend}
    df_results = pd.DataFrame(data=results, index=year)
    

    if(clm_scale):
        filename_out = path_results +'/results_'+ em_antr_scen + '_' + clm_run +'_' + oh_anomaly+ oh_run +'.txt'
    else:
        filename_out = path_results +'/results_'+ em_antr_scen + '_' + clm_run +'_unscaled_' + oh_anomaly + oh_run +'.txt'
    df_results.to_csv(filename_out)
    
    #Plotting (just to look if ok):
    if (plotteval):
        print('Start plotting...')
        
        plt.rcParams['font.size'] = 12
        
        noOfCols=2
        noOfRows=2
        fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(12,10))
        

            

        #Emissions:
        axes[0,0].plot(year,totemis,color='black',label='Total emission')
        axes[0,0].plot(df_natemis["natemis"],color='green',label='Natural emissions')
        axes[0,0].plot(df_emissions_ch4["Antr+BB"],color='dodgerblue',label='Antr.+ BB')
        axes[0,0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
        
        axes[0,0].set_title('Emissions')
        axes[0,0].set_ylabel("Tg/yr")
        axes[0,0].set_ylim([0,900]) 
        
        axes[0,0].fill([2008, 2017, 2017, 2008],
                       [550,550, 594, 594], fill=False, hatch='//',color='black',label='GMB TD 2008-2017')
        axes[0,0].legend()

        #Add the top-down numbers
        antr_bb_min = 81 + 207 + 22
        antr_bb_max = 131 + 240+ 36
        
        axes[0,0].fill([2008, 2017, 2017, 2008],
                       [antr_bb_min,antr_bb_min, antr_bb_max, antr_bb_max], fill=False, hatch='//',
                       color='dodgerblue',label='GMB TD 2008-2017')
        
        nat_min = 159 + 21
        nat_max = 200 + 50
        axes[0,0].fill([2008, 2017, 2017, 2008], [nat_min,nat_min, nat_max, nat_max],
                       fill=False, hatch='//',color='green',label='GMB TD 2008-2017')
        
        #Concentration
        axes[0,1].plot(conc_ch4,color='red',label='SCM_mean')
        axes[0,1].plot(data_conc['CH4'],color='black',label='Observed')
        
        axes[0,1].set_title('Concentration')
        axes[0,1].set_ylabel("ppbv")
        axes[0,1].set_ylim(bottom=750) 
        axes[0,1].legend()
        axes[0,1].axvspan(2000, 2007, alpha=0.2, color='lightgray')
        
        #Concentration trend
        axes[1,0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
        axes[1,0].axhline(y=0.0, color='gray', linestyle='-')
        
        data_trend = np.zeros(antyr)
        for yr in year:
            data_trend[yr-startyr] = data_conc['CH4'].loc[yr] - data_conc['CH4'].loc[yr-1]
            
        axes[1,0].plot(year,data_trend,color='black',label='Obs.')
        axes[1,0].plot(year,model_trend,color='red',label='SCM')
        axes[1,0].set_ylabel("ppbv/year")
        
        axes[0,0].set_xlim(left=startyr-10)
        axes[0,1].set_xlim(left=startyr-10)
        axes[1,0].set_xlim(left=startyr-10)
        
        
        fig.suptitle(em_antr_scen + ' Nat.anomalies: ' + clm_run +'(' + clm_anomaly + ')' + oh_run +'('+oh_anomaly+')')
        
        bbox=[0.2, 0, 0.9, 1]
        axes[1,1].axis('off')
        mpl_table = axes[1,1].table(cellText = df_meta.T.values, rowLabels = df_meta.columns, bbox=bbox, colLabels=df_meta.index)
        
        plt.show()
        plotteval = False
        exit()
        




    
        
    return()
