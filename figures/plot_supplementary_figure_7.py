import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams['font.size'] = 12

path = '/div/amoc/ragnhibs/ICOS/Python/ASCII/'

run_clm_list = ['CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4min',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max',
                'CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4min_q10ch4min']                

antrun = len(run_clm_list)
short_name = ['CRUJRA','fch4min','fch4max','q10min','q10max','q10max_fch4max','q10min_fch4min']

colorlist = ['mediumvioletred',
             'darkorange',
             'darkviolet',
             'peru',
             'deeppink',
             'yellowgreen',
             'mediumpurple',
             'green',
             'green']


#Make figure: 
noOfCols=1
noOfRows=1 
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(12,6))

for run in np.arange(0,antrun):
    filename = 'regional_FCH4_' +run_clm_list[run] + '.txt'
    data = pd.read_csv(path+filename,index_col=0)
    print(filename)
    print(data.columns)
    print(data.Global)

    mean_val = data.Global.loc[2000:2007].mean()
    anomaly = data.Global - mean_val
    print(anomaly)
    print(mean_val)
    if run == 0:
        linethick = 2
    else:
        linethick = 1
    axes.plot(anomaly,'-',linewidth=linethick,
              color=colorlist[run],zorder = 0,
              label=short_name[run]+' ['+ "{0:.0f}".format(mean_val) +' Tg yr$^{-1}$]')
    
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

plt.text(2017, -11, 'ElNino',color='red')
plt.text(2017, -13, 'LaNina',color='blue')


axes.set_title('Anomalies net emissions (relative to 2000-2007)')
axes.set_ylabel("Emission anomalies [Tg yr$^{-1}$]")    
axes.set_ylim([-20,25])
axes.set_xlim([1990,2020.5])


plt.minorticks_on()

axes.axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes.axhline(y=0,lw=0.5,color='k')



axes.legend(loc='upper left',ncol=2)
plt.show()
