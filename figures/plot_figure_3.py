import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['figure.dpi'] = 300

anom_year = 2000

path = '/div/qbo/users/ragnhibs/Methane/OH/'

scen = 'aerocom_historical'
filename = path + 'OsloCTM3/ForBoxModel/OsloCTM3_OH_unint_' + scen + '.txt'
data_met = pd.read_csv(filename, index_col=0)
val_ref =data_met.loc[anom_year] 
data_met = data_met.div(val_ref)


label_met='OsloCTM3 (CEDS17) variable meteorology'
print(data_met)

scen = 'histO3'
filename = path + 'OsloCTM3/ForBoxModel/OsloCTM3_OH_unint_' + scen + '.txt'
data_const_met= pd.read_csv(filename, index_col=0)
label_const_met='OsloCTM3 (CEDS17) fixed meteorology (Year 2010)'
val_ref =data_const_met.loc[anom_year] 
data_const_met = data_const_met.div(val_ref)


scen = 'histO3_ceds2021'
filename = path+'OsloCTM3/ForBoxModel/OsloCTM3_OH_unint_' + scen + '.txt'
data_const_met_ceds21= pd.read_csv(filename, index_col=0)
label_const_met_ceds21='OsloCTM3 (CEDS21+COVID)'

val_ref_ceds21 =data_const_met_ceds21.loc[anom_year] 
data_const_met_ceds21 = data_const_met_ceds21.div(val_ref)

#AerChemMIP
filename = path + 'DataFromOthers/ForBoxModel/AerChemMIP_UK_OH.txt'
data_UK = pd.read_csv(filename, index_col=0)
label_UK = 'AerChemMIP: UKESM1-0-LL'

filename = path + 'DataFromOthers/ForBoxModel/AerChemMIP_GFDL_OH.txt'
data_GFDL = pd.read_csv(filename, index_col=0)
label_GFDL = 'AerChemMIP: GFDL-ESM4'

filename = path + 'DataFromOthers/ForBoxModel/AerChemMIP_CESM2-WACCM_OH.txt'
data_CESM2WACCM = pd.read_csv(filename, index_col=0)
label_CESM2WACCM = 'AerChemMIP: CESM2-WACCM'


#CCMI
filename = path + 'DataFromOthers/ForBoxModel/CCMI_modelmin_OH.txt'
data_CCMI_min = pd.read_csv(filename, index_col=0)
data_CCMI_min = data_CCMI_min.loc[1960:]

filename = path + 'DataFromOthers/ForBoxModel/CCMI_modelmax_OH.txt'
data_CCMI_max = pd.read_csv(filename, index_col=0)
data_CCMI_max = data_CCMI_max.loc[1960:]



enso_yval_max = 0.927
enso_yval_min = 0.92
enso_val_text = [0.93,0.939]

ylabeltext = 'Global OH relative to year 2000'



plt.rcParams['font.size'] = 14
noOfCols=2
noOfRows=1
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(14,6.5))
axes[0].minorticks_on()
axes[1].minorticks_on()


print(data_GFDL.shape)

aerchemip = np.zeros([2,len(data_UK.values)])
aerchemip[0,:] = data_UK['OHrel'].values
aerchemip[1,:] = data_CESM2WACCM['OHrel'].values
aerchemip = np.vstack((aerchemip,data_GFDL['OHrel'].values))#

axes[0].fill_between(data_UK.index, np.amax(aerchemip,axis=0), np.amin(aerchemip,axis=0),facecolor='darkgreen',alpha= 0.2, label='AerChemMIP')
axes[1].fill_between(data_UK.index, np.amax(aerchemip,axis=0), np.amin(aerchemip,axis=0),facecolor='darkgreen',alpha= 0.2) 


axes[0].fill_between(data_CCMI_min.index,data_CCMI_min['OHrel'].values,data_CCMI_max['OHrel'].values ,facecolor='darkblue',alpha= 0.2, label='CCMI')
axes[1].fill_between(data_CCMI_min.index,data_CCMI_min['OHrel'].values,data_CCMI_max['OHrel'].values ,facecolor='darkblue',alpha= 0.2) #, label='CCMI')




axes[0].plot(data_met,'-',color='darkblue',label=label_met)
axes[0].plot(data_const_met,'--d',color='darkblue',label=label_const_met)
axes[0].text(0.02, 0.95, '(a)',transform=axes[0].transAxes,fontsize=15)



axes[1].plot(data_met,'-',color='darkblue')
axes[1].plot(data_const_met,'--d',color='darkblue')
axes[1].plot(data_const_met_ceds21,'--x',color='darkred',label=label_const_met_ceds21)

axes[1].text(0.02, 0.95, '(b)',transform=axes[1].transAxes,fontsize=15)

axes[0].set_xlim([1845,2025])
axes[1].set_xlim([1965,2025])
axes[0].set_ylim([0.90,1.07])
axes[1].set_ylim([0.90,1.07])
axes[0].axvspan(2000, 2007, alpha=0.2, color='lightgray')
axes[1].axvspan(2000, 2007, alpha=0.2, color='lightgray')

axes[0].legend(frameon=False,fontsize=12,loc='lower left')
axes[1].legend(frameon=False,fontsize=12,loc='lower left')
axes[0].set_ylabel(ylabeltext)
axes[1].set_ylabel(ylabeltext)


plt.savefig('figures/' + "figure3.png")

plt.show()


exit()


