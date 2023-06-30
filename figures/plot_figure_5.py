import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Script preparing data to the box model and for figure 5.
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 16

path = 'ASCII/'

run_clm_list = ['CNTRv5_I2000Clm50BgcCrop_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCru_f09_g16_VER2']

antrun = len(run_clm_list)
short_name = ['GSWP3','CRUJRA','CRUNCEP']
colorlist = ['darkblue','mediumvioletred','forestgreen']

#Make figure: 
noOfCols=1
noOfRows=2 
fig, ax = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(11,18))
axes = ax[0]

for run in np.arange(0,antrun):
    filename = 'regional_FCH4_' +run_clm_list[run] + '.txt'
    data = pd.read_csv(path+filename,index_col=0)
    print(filename)
    print(data.columns)

    mean_val = data.Global.loc[2000:2007].mean()
    anomaly = data.Global - mean_val
    print(anomaly)
    print(mean_val)
    axes.plot(anomaly,color=colorlist[run],
              label=short_name[run]+' ['+ "{0:.0f}".format(mean_val) +' Tg yr$^{-1}$]')


    
    filename = 'ASCII/annual_totCH4_for_box_model_' + run_clm_list[run] + '.txt'
    print(filename)
    df = pd.DataFrame(data.Global.values,columns=['Annual'],index=data.index)

    #Write data to be used in the box model.
    #df.to_csv(filename)


#Add enso:             
#https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php
#Data here:
#Seasonal ERSSTv5 (centered base periods) "Oceanic Nino Index" or the 3-month running average in Nino 3.4 (5oNorth-5oSouth) (170-120oWest))
#Data (Oceanic Nino Index)
#https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt

enso_file = '/div/amoc/ragnhibs/ICOS/Python/DataFromOthers/ENSO/enso_index_v060523.txt'
enso_data = pd.read_csv(enso_file,delim_whitespace=True,index_col=None)
print(enso_data)

print(enso_data.columns)

len_enso = len(enso_data.YR)
enso_years = [1950]
for x in range(1,len_enso): enso_years.append(enso_years[x-1]+1.0/12.0)

enso_data.insert(0, "Year", enso_years,allow_duplicates=False) 

enso_data.set_index('Year',inplace=True)

print(enso_data)


enso_val=enso_data.ANOM
print(enso_val)
enso_pos = enso_val.copy()
enso_pos[enso_pos<0.5]=np.nan
enso_neg = enso_val.copy()
enso_neg[enso_neg>-0.5]=np.nan

print(enso_neg)

axes.fill_between(enso_val.index-0.5, -15, -14, where=(enso_val > 0.5),alpha=.6,color='red')
axes.fill_between(enso_val.index-0.5, -15, -14, where=(enso_val < -0.5),alpha=.6,color='blue')
axes.axhline(y=-14,lw=0.2,color='k')
axes.axhline(y=-15,lw=0.2,color='k')

axes.text(2015, -11, 'ElNino',color='red')
axes.text(2015, -13, 'LaNina',color='blue')



axes.set_title('(a) Anomalies net emissions (relative to 2000-2007)',loc='left')
axes.set_ylabel("Emission anomalies [Tg yr$^{-1}]$")    
axes.set_ylim([-20,30])
axes.set_xlim([1990,2020.5])


axes.minorticks_on()

axes.axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes.axhline(y=0,lw=0.5,color='k')


#ADD sensitivity tests:
run_clm_list = ['CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max']


antrun = len(run_clm_list)
yr_sens = np.arange(1990,2020)
antyr = len(yr_sens)
sens_anomaly = np.zeros([antyr,antrun])
print(sens_anomaly)


for run in np.arange(0,antrun):
    filename = 'regional_FCH4_' +run_clm_list[run] + '.txt'
    data = pd.read_csv(path+filename,index_col=0)
    print(filename)
    print(data.columns)
    print(data.Global)

    mean_val = data.Global.loc[2000:2007].mean()
    anomaly = data.Global - mean_val
    sens_anomaly[:,run] = anomaly
    print(anomaly)
    print(mean_val)


    filename = 'ASCII/annual_totCH4_for_box_model_' + run_clm_list[run] + '.txt'
    print(filename)
    df = pd.DataFrame(data.Global.values,columns=['Annual'],index=data.index)
    #df.to_csv(filename)


max_anomalies = np.amax(sens_anomaly,axis=1)
min_anomalies = np.amin(sens_anomaly,axis=1)
axes.fill_between(yr_sens, min_anomalies, max_anomalies,facecolor=colorlist[1],alpha= 0.1,zorder=0)

     





############

#For panel b)
axes=ax[1]
run_clm_list = ['CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2']

antrun = len(run_clm_list)
#short_name = ['CRUJRA','GWSP3','CRUNCEP']
colorlist = ['mediumvioletred','darkblue','forestgreen']


#Make figure: 
for run in np.arange(0,antrun):
    filename = 'regional_wetland_FCH4_' +run_clm_list[run] + '.txt'
    data = pd.read_csv('ASCII/'+filename,index_col=0)
    print(filename)
    print(data.columns)
    print(data.Global)

    mean_val = data.Global.loc[2000:2007].mean()
    anomaly = data.Global - mean_val
    print(anomaly)
    print(mean_val)
    axes.plot(anomaly,marker='o',ls='--', color=colorlist[run],label='CLM (CRUJRA) [' + "{0:.0f}".format(mean_val) +' Tg yr$^{-1}$]')

    #Add SWAMPS wetland
    filename = 'regional_wetland_use_swamps_FCH4_' +run_clm_list[run] + '.txt'
    data = pd.read_csv('ASCII/'+filename,index_col=0)
    print(filename)
    print(data.columns)
    print(data.Global)

    mean_val = data.Global.loc[2000:2007].mean()
    anomaly = data.Global - mean_val
    print(anomaly)
    print(mean_val)
    axes.plot(anomaly,marker='d',lw=1, color=colorlist[run], label='WAD2M [' + "{0:.0f}".format(mean_val) +' Tg yr$^{-1}$]')


    #Add SWAMPS wetland
    filename = 'regional_wetland_use_oldgmb_FCH4_' +run_clm_list[run] + '.txt'
    data = pd.read_csv('ASCII/'+filename,index_col=0)
    print(filename)
    print(data.columns)
    print(data.Global)

    mean_val = data.Global.loc[2000:2007].mean()
    anomaly = data.Global - mean_val
    print(anomaly)
    print(mean_val)
    axes.plot(anomaly,marker='d',lw=1, color='blue', label='SWAMPS-GLWD [' + "{0:.0f}".format(mean_val) +' Tg yr$^{-1}$]')


axes.fill_between(enso_val.index-0.5, -15, -14, where=(enso_val > 0.5),alpha=.6,color='red')
axes.fill_between(enso_val.index-0.5, -15, -14, where=(enso_val < -0.5),alpha=.6,color='blue')
axes.axhline(y=-14,lw=0.2,color='k')
axes.axhline(y=-15,lw=0.2,color='k')

axes.text(2015, -11, 'ElNino',color='red')
axes.text(2015, -13, 'LaNina',color='blue')
#print(enso_years[enso_pos.index.values])

#ADD sensitivity tests:
run_clm_list = ['CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max']

antrun = len(run_clm_list)
yr_sens = np.arange(1990,2020)
antyr = len(yr_sens)
sens_anomaly = np.zeros([antyr,antrun])
print(sens_anomaly)
#print(yr_sens)

for run in np.arange(0,antrun):
    filename = 'regional_wetland_FCH4_' +run_clm_list[run] + '.txt'
    data = pd.read_csv('ASCII/'+filename,index_col=0)
    print(filename)
    print(data.columns)
    print(data.Global)

    mean_val = data.Global.loc[2000:2007].mean()
    anomaly = data.Global - mean_val
    sens_anomaly[:,run] = anomaly
    print(anomaly)
    print(mean_val)

max_anomalies = np.amax(sens_anomaly,axis=1)
min_anomalies = np.amin(sens_anomaly,axis=1)
axes.fill_between(yr_sens, min_anomalies, max_anomalies,facecolor=colorlist[0],alpha= 0.1,zorder=0)

#ADD CHANDRA
#Data provided by Prabir Patra 
path = '/div/qbo/users/ragnhibs/Methane/WETLAND/DataFromOthers/Chandra_2020/data_fig5d/'
file1 = 'p01_ch4_latemis_WetlandCao_lr.txt'
file2 = 'p01_ch4_latemis_Wetland_WH_lr.txt'

data_emis1 = pd.read_csv(path+file1,delimiter=' ',index_col=0,header=1)
data_emis2 = pd.read_csv(path+file2,delimiter=' ',index_col=0,header=1)

glob1 = data_emis1['Glob']
glob2 = data_emis2['Glob']

print(0.5*(glob1.mean()+glob2.mean()))


filename = 'ASCII/annual_totCH4_for_box_model_' + 'VISIT-CAO' + '.txt'
print(filename)
df = pd.DataFrame(glob1.values,columns=['Annual'],index=glob1.index)
#df.to_csv(filename)

filename = 'ASCII/annual_totCH4_for_box_model_' + 'VISIT-VH' + '.txt'
print(filename)
df = pd.DataFrame(glob2.values,columns=['Annual'],index=glob2.index)
#df.to_csv(filename)



mean_val1 = glob1.loc[2000:2007].mean()
mean_val2 = glob2.loc[2000:2007].mean()
anomaly1 = glob1 - mean_val1
anomaly2 = glob2 - mean_val2

#Plot in panel b)

ax[1].plot(anomaly1,'-',color='limegreen',zorder=0,
          label='VISIT (Cao) ['+ "{0:.0f}".format(mean_val1) +' Tg yr$^{-1}$]')
ax[1].plot(anomaly2,'-',color='lightgreen',zorder=0,
          label='VISIT (WH) ['+ "{0:.0f}".format(mean_val2) +' Tg yr$^{-1}$]')


################
print('Add Zhang')

path = '/div/qbo/users/oivinho/WORK/ReGAME/OH_vs_isotopes/emis_wetland_Zhang2023/'

file1 = 'LPJ_mmch4e_MERRA2_2000-2021_globalannualmeans.txt'
file2 = 'LPJ_mmch4e_CRU_2000-2021_globalannualmeans.txt'

data_emis1 = pd.read_csv(path+file1,delimiter=',',skipinitialspace=True, index_col=0,header=0)
data_emis2 = pd.read_csv(path+file2,delimiter=',',skipinitialspace=True,index_col=0,header=0)

glob1 = data_emis1['Emis']
glob2 = data_emis2['Emis']

filename = 'ASCII/annual_totCH4_for_box_model_' + 'Zhang-MERRA2' + '.txt'
print(filename)
df = pd.DataFrame(glob1.loc[slice(2000,2020)].values,columns=['Annual'],index=glob1.loc[slice(2000,2020)].index)
#df.to_csv(filename)

filename = 'ASCII/annual_totCH4_for_box_model_' + 'Zhang-CRU' + '.txt'
print(filename)
df = pd.DataFrame(glob2.loc[slice(2000,2020)].values,columns=['Annual'],index=glob2.loc[slice(2000,2020)].index)
#df.to_csv(filename)


mean_val1 = glob1.loc[2000:2007].mean()
mean_val2 = glob2.loc[2000:2007].mean()
anomaly1 = glob1 - mean_val1
anomaly2 = glob2 - mean_val2

print(anomaly1)
print(anomaly2)

#Plot in panel b)
ax[1].plot(anomaly1,'-',color='firebrick',zorder=-1,
          label='LPJ_wsl (MERRA2) ['+ "{0:.0f}".format(mean_val1) +' Tg yr$^{-1}$]')
ax[1].plot(anomaly2,'-',color='maroon',zorder=-1,
          label='LPJ_wsl (CRU) ['+ "{0:.0f}".format(mean_val2) +' Tg yr$^{-1}$]')



axes.set_title('(b) Anomalies wetland emissions (relative to 2000-2007)',loc='left')
axes.set_ylabel("Emission anomalies [Tg yr$^{-1}$]")    
axes.set_ylim([-20,30])
axes.set_xlim([1990,2020.5])

axes.minorticks_on()
axes.axvspan(2000, 2007, alpha=0.2, color='lightgray')

axes.axhline(y=0,lw=0.5,color='k')

ax[0].legend(fontsize=14,frameon=False)
ax[1].legend(fontsize=14,ncol=2, frameon=False)


plt.savefig('figures/' + "figure5.png")
#plt.show()
