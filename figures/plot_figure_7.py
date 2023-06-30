import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Script for generating Figure 7 and Supplementary Figure 8.
#Global emission numbers for the different inventories must be pre-calculated.

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 14
plt.rcParams.update({'errorbar.capsize': 5})
noOfCols=2
noOfRows=1
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols,sharex=True, figsize=(12,8))

#**********************IPCC Lamarque*******************************
filepath = '/uio/kant/div-cicero-u1/ragnhibs/CICERO/SUPER-SIS/IDL/ASCII/'
file = 'anthropogenic_IPCC_NO.txt'
factor = 1.533333333
data_emis = pd.read_csv(filepath+file,delimiter=' ',index_col=0,header=0,skipinitialspace=True)
data_emis.index.name = 'Year'

ipcc_nox  = data_emis*factor

file = 'shipping_IPCC_NO2.txt'
data_emis = pd.read_csv(filepath+file,delimiter='\t',index_col=0,header=0,skipinitialspace=True)
data_emis.index.name = 'Year'
print(data_emis)

ipcc_nox  = ipcc_nox + data_emis.values

file = 'aviation_IPCC_NO2.txt'
data_emis = pd.read_csv(filepath+file,delimiter='\t',index_col=0,header=0,skipinitialspace=True)
data_emis.index.name = 'Year'
print(data_emis)
ipcc_nox  = ipcc_nox + data_emis.values

axes[0].plot(ipcc_nox,color='gray',label='RCP historical')


file = 'anthropogenic_IPCC_CO.txt'
factor = 1.0
data_emis = pd.read_csv(filepath+file,delimiter=' ',index_col=0,header=0,skipinitialspace=True)
data_emis.index.name = 'Year'

ipcc_co  = data_emis*factor

file = 'shipping_IPCC_CO.txt'
data_emis = pd.read_csv(filepath+file,delimiter='\t',index_col=0,header=0,skipinitialspace=True)
data_emis.index.name = 'Year'
print(data_emis)

ipcc_co  = ipcc_co + data_emis.values

axes[1].plot(ipcc_co,color='gray',label='RCP historical')
print(ipcc_nox)
print(ipcc_co)

ratio_ipcc = ipcc_nox.div(ipcc_co.values)
print(ratio_ipcc)

axes[0].set_xlim([1970,2030])

axes[0].set_ylabel('Emissions NO$_2$ [Tg]')
axes[1].set_ylabel('Emissions CO [Tg]')


axes[0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes[1].axvspan(2000, 2007, alpha=0.2, color='lightgray')


######################## RCP #########################################
file = 'anthropogenic_RCP_NO2.txt'
data_emis = pd.read_csv(filepath+file,delimiter='\t',index_col=0,header=0)
print(filepath+file)
data_emis.index.name = 'Year'
print(data_emis)
rcps_nox  = data_emis
axes[0].plot(rcps_nox['RCP6.0'],color='gray',linestyle='--',linewidth=0.5,label='RCPs')
axes[0].plot(rcps_nox,color='gray',linestyle='--',linewidth=0.5)

file = 'anthropogenic_RCP_CO.txt'
data_emis = pd.read_csv(filepath+file,delimiter='\t',index_col=0,header=0)
print(filepath+file)
data_emis.index.name = 'Year'
print(data_emis)
rcps_co  = data_emis
axes[1].plot(rcps_co['RCP6.0'],color='gray',linestyle='--',linewidth=0.5,label='RCPs')
axes[1].plot(rcps_co,color='gray',linestyle='--',linewidth=0.5)

ratio_rcp = rcps_nox.div(rcps_co)

########################### CEDS v2016 ########################################
filepath = '/div/qbo/users/ragnhibs/Methane/INPUT/EMISSIONS/CEDS_emissions/'
file = 'NOx_CEDS_emissions_by_country_v2016_07_26.csv'

data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=None,header=0,skiprows=0).T
#ktNO2 -> Tg NO2
data_emis = data_emis.drop(['em','country','units'])
data_emis.index.name = 'Year'

ceds_v2016_year = np.arange(1750,2015)
ceds_v2016_nox = data_emis.sum(axis=1).mul(1000*1000*1000*1e-12)
axes[0].plot(ceds_v2016_year,ceds_v2016_nox,color='darkblue',label='CEDS-2017')


file = 'CO_CEDS_emissions_by_country_v2016_07_26.csv'

data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=None,header=0,skiprows=0).T
#ktCO -> Tg CO
data_emis = data_emis.drop(['em','country','units'])
data_emis.index.name = 'Year'

ceds_v2016_year = np.arange(1750,2015)
ceds_v2016_co = data_emis.sum(axis=1).mul(1000*1000*1000*1e-12)
axes[1].plot(ceds_v2016_year,ceds_v2016_co,color='darkblue',label='CEDS-2017')

ratio_ceds_v2016 = ceds_v2016_nox/ceds_v2016_co


#########################SSPs################################

ssplist = ['SSP119','SSP126','SSP245','SSP370','SSP3lowNTCF','SSP434','SSP460','SSP534','SSP585']
#plot alternative data based on the gridded file:
for scen in ssplist:
    fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_CO_CEDS_SCENARIOS_'+scen+'.csv'
    df_scen_co = pd.read_csv(fileceds,index_col=0)
    df_scen_co.name = scen
    print(df_scen_co)
    df_scen_co = df_scen_co.rename(columns={"Emis":scen})
    print(df_scen_co)
    if scen == 'SSP119':
        axes[1].plot(df_scen_co,'--',color='darkblue',linestyle='--',linewidth=0.5,label='SSPs')
        df_scen_all_co = df_scen_co
        print(df_scen_all_co)
    else:
        axes[1].plot(df_scen_co,'--',color='darkblue',linestyle='--',linewidth=0.5)
        df_scen_all_co =  pd.concat([df_scen_all_co, df_scen_co], axis=1) 

    fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_NOx_CEDS_SCENARIOS_'+scen+'.csv'
    df_scen_ant = pd.read_csv(fileceds,index_col=0)
    fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_aviationNOx_CEDS_SCENARIOS_'+scen+'.csv'
    df_scen_avi = pd.read_csv(fileceds,index_col=0)
    df_scen_nox = df_scen_ant+df_scen_avi
    df_scen_nox = df_scen_nox.rename(columns={"Emis":scen})
    if scen == 'SSP119':
        axes[0].plot(df_scen_nox,'--',color='darkblue',linestyle='--',linewidth=0.5,label='SSPs')
        df_scen_all_nox = df_scen_nox
    else:
        axes[0].plot(df_scen_nox,'--',color='darkblue',linestyle='--',linewidth=0.5)
        df_scen_all_nox =  pd.concat([df_scen_all_nox, df_scen_nox], axis=1) 

print(df_scen_all_co)
print(df_scen_all_nox)
ratio_ssp = df_scen_all_nox.div(df_scen_all_co)

        



#####################################CEDS2019###########################################
filepath = '/div/qbo/users/ragnhibs/Methane/INPUT/EMISSIONS/CEDS_emissions/'
file = 'CEDS_NOx_emissions_by_country_v_2019_12_23.csv'

data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=None,header=0,skiprows=0).T
#ktNO2 -> Tg NO2

data_emis = data_emis.drop(['em','iso','units'])
data_emis.index.name = 'Year'

ceds_v2019_year = np.arange(1750,2015)
ceds_v2019_nox = data_emis.sum(axis=1).mul(1000*1000*1000*1e-12)

file = 'CEDS_CO_emissions_by_country_v_2019_12_23.csv'

data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=None,header=0,skiprows=0).T
#ktCO -> Tg CO
data_emis = data_emis.drop(['em','iso','units'])
data_emis.index.name = 'Year'

ceds_v2019_year = np.arange(1750,2015)
ceds_v2019_co = data_emis.sum(axis=1).mul(1000*1000*1000*1e-12)


ratio_ceds_v2019 = ceds_v2019_nox/ceds_v2019_co


#####################################CEDS v2021#####################################
filepath = '/div/qbo/users/ragnhibs/Methane/INPUT/EMISSIONS/CEDS_emissions/'
file = 'NOx_global_CEDS_emissions_by_sector_2021_02_05.csv'

data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=None,header=0,skiprows=0).T
#ktNO2 -> Tg NO2

print(data_emis.index)
data_emis = data_emis.drop(['em','sector','units'])
data_emis.index.name = 'Year'
index = data_emis.index.values
for i,year in enumerate(index):
    year = year.split("X")
    index[i] = year[-1]
    
data_emis.index = index.astype(int)

ceds_v2021_nox = data_emis.sum(axis=1).mul(1000*1000*1000*1e-12)
axes[0].plot(ceds_v2021_nox,color='lightblue',label='CEDS_v2021')


file = 'CO_global_CEDS_emissions_by_sector_2021_02_05.csv'

data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=None,header=0,skiprows=0).T
#ktCO -> Tg CO
data_emis = data_emis.drop(['em','sector','units'])
data_emis.index.name = 'Year'
index = data_emis.index.values
for i,year in enumerate(index):
    year = year.split("X")
    index[i] = year[-1]
    
data_emis.index = index.astype(int)


ceds_v2021_co = data_emis.sum(axis=1).mul(1000*1000*1000*1e-12)
axes[1].plot(ceds_v2021_co,color='lightblue',label='CEDS-2021')

ratio_ceds_v2021 = ceds_v2021_nox/ceds_v2021_co


############################COVID-19###########################
#plot alternative data based on the gridded file:
fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_NOx_CEDS21_COVID.csv'
df_covid_nox = pd.read_csv(fileceds,index_col=0)
fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_aviation_NOx_CEDS21_COVID.csv'
df_covid_nox_avi = pd.read_csv(fileceds,index_col=0)
fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_CO_CEDS21_COVID.csv'
df_covid_co = pd.read_csv(fileceds,index_col=0)

covid_nox = df_covid_nox.loc[2020] + df_covid_nox_avi.loc[2020] 
covid_co = df_covid_co.loc[2020]

axes[0].plot(2020, covid_nox.values ,linestyle='none',marker='*',color='lightblue',label='COVID19est')
axes[1].plot(2020, covid_co.values ,linestyle='none',marker='*',color='lightblue',label='COVID19est')
ratio_covid = (covid_nox)/(covid_co)


print('Tg decrease in NOx emissions (Tg/%)')
print( covid_nox -ceds_v2021_nox.loc[2019])
print( (covid_nox -ceds_v2021_nox.loc[2019])/ceds_v2021_nox.loc[2019]*100)

print('Tg decrease in CO emissions (Tg/%)')
print( covid_co - ceds_v2021_co.loc[2019])
print( (covid_co - ceds_v2021_co.loc[2019])/ceds_v2021_co.loc[2019]*100)


######################EDGARv5###############################
filepath = '/uio/kant/div-cicero-u1/ragnhibs/CICERO/SUPER-SIS/IDL/ASCII/'
file = 'anthropogenic_EDGARv50_NOx.txt'
edgar_v5_nox = pd.read_csv(filepath+file,delimiter=',',header=None,index_col=0)
edgar_v5_nox =edgar_v5_nox*0.001
axes[0].plot(edgar_v5_nox,color='salmon',label='EDGARv5')

file = 'anthropogenic_EDGARv50_CO.txt'
edgar_v5_co = pd.read_csv(filepath+file,delimiter=',',header=None,index_col=0)
edgar_v5_co = edgar_v5_co*0.001
axes[1].plot(edgar_v5_co,color='salmon',label='EDGARv5')

ratio_edgar_v5 = edgar_v5_nox.div(edgar_v5_co)


print(data_emis)





########################ECLIPSEv6###########################
filepath = '/div/qbo/users/ragnhibs/Methane/INPUT/EMISSIONS/'

file = 'ECLIPSEv6_NO2.txt'
eclipse_v6_nox = pd.read_csv(filepath+file,delimiter='\t',header=None,index_col=0)
eclipse_v6_nox =eclipse_v6_nox*0.001
axes[0].plot(eclipse_v6_nox,color='darkviolet',label='ECLIPSEv6')
file = 'ECLIPSEv6_CO.txt'
eclipse_v6_co = pd.read_csv(filepath+file,delimiter='\t',header=None,index_col=0)
eclipse_v6_co = eclipse_v6_co*0.001
axes[1].plot(eclipse_v6_co,color='darkviolet',label='ECLIPSEv6')
ratio_eclipse_v6 = eclipse_v6_nox.div(eclipse_v6_co)


#########################SSPs################################
#filepath = '/uio/kant/div-cicero-u1/ragnhibs/CICERO/SUPER-SIS/IDL/ASCII/'

dataset = 'CMIP6-BB'
fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_biomassburning_NOx_CMIP6.csv' 
cmip6_bb_no2 = pd.read_csv(fileceds,index_col=0)
print(cmip6_bb_no2)

fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_biomassburning_CO_CMIP6.csv' 
cmip6_bb_co = pd.read_csv(fileceds,index_col=0)
print(cmip6_bb_co)

axes[0].plot(cmip6_bb_no2,color='forestgreen',label=dataset)
axes[1].plot(cmip6_bb_co,color='forestgreen',label=dataset)

dataset = 'BB SSP2-4.5'
fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_biomassburning_NOx_SSP245.csv' 
ssp_bb_no2 = pd.read_csv(fileceds,index_col=0)
print(cmip6_bb_no2)

fileceds = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_biomassburning_CO_SSP245.csv' 
ssp_bb_co = pd.read_csv(fileceds,index_col=0)
print(cmip6_bb_co)

axes[0].plot(ssp_bb_no2,'--',color='forestgreen',label=dataset)
axes[1].plot(ssp_bb_co,'--',color='forestgreen',label=dataset)

####################GFED#################################################
filepath = '/div/qbo/users/ragnhibs/Methane/INPUT/EMISSIONS/'
file =  'gfed_v41s_no2_110521.csv'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=1)
data_emis.index.name = 'Year'
print(data_emis)
gfed_no2  = data_emis['GFED_v41s']
axes[0].plot(gfed_no2,color='lightgreen',label='GFEDv4.1s')

file =  'gfed_v41s_co_110521.csv'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=1)
data_emis.index.name = 'Year'
print(data_emis)
gfed_co  = data_emis['GFED_v41s']
axes[1].plot(gfed_co,color='lightgreen',label='GFEDv4.1s')

######################END OF PLOTTING DATA#################################
axes[0].set_ylim(bottom=0)
axes[1].set_ylim(bottom=0)
axes[1].legend(ncol=2,frameon=False,loc='lower left')



plt.savefig('figures/' + "supplementary_figure_8.png")

noOfCols=1
noOfRows=1
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols,sharex=True, figsize=(8,7))

axes.plot(ratio_ipcc,color='gray',label='RCP historical')
axes.plot(ratio_rcp,color='gray',linestyle='--',linewidth=0.5)
axes.plot([-10,-10],[-10,-9],color='gray',linestyle='--',linewidth=0.5, label='RCPs')
axes.plot(ceds_v2016_year,ratio_ceds_v2016,color='darkblue',label='CEDS-2017')
axes.plot(ratio_ssp,color='darkblue',linestyle='--',linewidth=0.5)
axes.plot([-10,-10],[-10,-9],color='darkblue',linestyle='--',linewidth=0.5, label='SSPs')

axes.plot(ratio_ceds_v2021,color='lightblue',label='CEDS-2021')
axes.plot(2020, ratio_covid ,linestyle='none',marker='*',color='lightblue',label='COVID19est')
axes.plot(ratio_edgar_v5,color='salmon',label='EDGARv5')

axes.plot(ratio_eclipse_v6,color='darkviolet',label='ECLIPSEv6')

axes.set_ylabel('Anthropogenic NOx/CO emission ratio')
axes.axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes.set_xlim([1970,2030])
axes.set_ylim([0,0.35])
axes.legend(ncol=2,frameon=False,loc='lower left')

plt.savefig('figures/' + "figure7.png")


