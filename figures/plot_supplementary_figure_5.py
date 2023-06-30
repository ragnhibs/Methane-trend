import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

anom_year = 2000
path = '/div/qbo/users/ragnhibs/Methane/OH/'

scen = 'aerocom_historical'
filename = path + 'OsloCTM3/ForBoxModel/OsloCTM3_CH4lifetime_unint_' + scen + '.txt'
data_met = pd.read_csv(filename, index_col=0)
val_ref =data_met.loc[anom_year] 
data_met = data_met.div(val_ref)


label_met='OsloCTM3 (CEDS17) variable meteorology'
print(data_met)

scen = 'histO3'
filename = path + 'OsloCTM3/ForBoxModel/OsloCTM3_CH4lifetime_unint_' + scen + '.txt'
data_const_met= pd.read_csv(filename, index_col=0)
label_const_met='OsloCTM3 (CEDS17) fixed meteorology (Year 2010)'

val_ref =data_const_met.loc[anom_year] 
data_const_met = data_const_met.div(val_ref)


scen = 'histO3_ceds2021'
filename = path + 'OsloCTM3/ForBoxModel/OsloCTM3_CH4lifetime_unint_' + scen + '.txt'
data_const_met_ceds21= pd.read_csv(filename, index_col=0)
label_const_met_ceds21='OsloCTM3 (CEDS21+COVID)'

val_ref_ceds21 =data_const_met_ceds21.loc[2000] 
data_const_met_ceds21 = data_const_met_ceds21.div(val_ref_ceds21)




enso_yval_max = 0.925
enso_yval_min = 0.92
enso_val_text = [0.93,0.935]

ylabeltext = 'Methane lifetime relative to year 2000'



plt.rcParams['font.size'] = 14
noOfCols=2
noOfRows=1
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(14,6.5))
axes[0].minorticks_on()
axes[1].minorticks_on()

axes[0].plot(data_met,'-',color='darkblue',label=label_met)
axes[0].plot(data_const_met,'--d',color='darkblue',label=label_const_met)
axes[0].text(0.02, 0.95, '(a)',transform=axes[0].transAxes,fontsize=15)

axes[1].plot(data_met,'-',color='darkblue')#,label=label_met)
axes[1].plot(data_const_met,'--d',color='darkblue') #,label=label_const_met)
axes[1].text(0.02, 0.95, '(b)',transform=axes[1].transAxes,fontsize=15)
axes[1].plot(data_const_met_ceds21,'--x',color='darkred',label=label_const_met_ceds21)


axes[0].set_xlim([1845,2025])
axes[1].set_xlim([1965,2025])
axes[0].set_ylim([0.91,1.04])
axes[1].set_ylim([0.91,1.04])
axes[0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes[1].axvspan(2000, 2007, alpha=0.2, color='lightgray')

axes[0].legend(frameon=False,fontsize=12)
axes[1].legend(frameon=False,fontsize=12,loc='lower left')
axes[0].set_ylabel(ylabeltext)
axes[1].set_ylabel(ylabeltext)


#Add enso:             
#https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php
#Data here:
#Seasonal ERSSTv5 (centered base periods) "Oceanic Nino Index" or the 3-month running average in Nino 3.4 (5oNorth-5oSouth) (170-120oWest))
#Data (Oceanic Nino Index)
#https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
'''
enso_file = '/div/amoc/ragnhibs/ICOS/Python/DataFromOthers/ENSO/enso_index_v130121.txt'
enso_data = pd.read_csv(enso_file,delim_whitespace=True,index_col=None)

len_enso = len(enso_data.YR)
enso_years = [1950]
for x in range(1,len_enso): enso_years.append(enso_years[x-1]+1.0/12.0)
enso_data.insert(0, "Year", enso_years,allow_duplicates=False) 
enso_data.set_index('Year',inplace=True)
enso_val=enso_data.ANOM

enso_pos = enso_val.copy()
enso_pos[enso_pos<0.5]=np.nan
enso_neg = enso_val.copy()
enso_neg[enso_neg>-0.5]=np.nan

#print(enso_neg)
#https://stackoverflow.com/questions/50722612/shade-region-of-interest-in-matplotlib-chart
axes[1].fill_between(enso_val.index, enso_yval_min, enso_yval_max, where=(enso_val > 0.5),color='red',alpha=.6)
axes[1].fill_between(enso_val.index, enso_yval_min, enso_yval_max, where=(enso_val < -0.5),color='blue',alpha=.6)
axes[1].axhline(y=enso_yval_min,lw=0.2,color='k')
axes[1].axhline(y=enso_yval_max,lw=0.2,color='k')


axes[1].text(2015, enso_val_text[0], 'ElNino',color='red',alpha=.6)
axes[1].text(2015, enso_val_text[1], 'LaNina',color='blue',alpha=.6)
#print(enso_years[enso_pos.index.values])
'''


plt.show()


exit()


