import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['figure.dpi'] = 300

#This script generate figure 2 and supplementary figure 1 and
#prepare input fields to be used in the box model. The global
#emission numbers (sources described in the main manuscript must
#first be calculated).

#Filepath for global emission numbers: 
filepath = '/div/qbo/users/ragnhibs/Methane/INPUT/EMISSIONS/'

plt.rcParams['font.size'] = 14
plt.rcParams.update({'errorbar.capsize': 5})
noOfCols=1
noOfRows=1
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(8,7))

#IPCC Lamarque
file = 'anthropogenic_IPCC_CH4.txt'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=0) #,skipinitialspace=True)
data_emis.index.name = 'Year'
print(data_emis)
ipcc  = data_emis
axes.plot(ipcc,color='gray',label='RCP historical')

#RCP
file = 'anthropogenic_RCP_CH4.txt'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=0)
data_emis.index.name = 'Year'
print(data_emis)
rcps  = data_emis
axes.plot(rcps['RCP6.0'].loc[:2020],color='gray',linestyle='--',label='RCPs')
axes.plot(rcps.loc[:2020],color='gray',linestyle='--')


#CEDS
file = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_CH4_CEDS17.csv'
data_emis = pd.read_csv(file,delimiter=',',index_col=0,header=0)
data_emis.index.name = 'Year'
print(data_emis)
ceds_17 = data_emis
axes.plot(ceds_17['Emis'],color='darkblue',label='CEDS-2017')


file = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_CH4_CEDS21.csv'
data_emis = pd.read_csv(file,delimiter=',',index_col=0,header=0)
data_emis.index.name = 'Year'
print(data_emis)
ceds_21 = data_emis
axes.plot(ceds_21['Emis'],color='lightblue',label='CEDS-2021')


file = 'CEDS_diff_versions_to_qbo.csv'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=0)
data_emis.index.name = 'Year'
print(data_emis)
ceds  = data_emis*0.001

#SSPs
file = 'SSPs_to_qbo.csv'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=1)
data_emis.index.name = 'Year'
print(data_emis)

ssps  = data_emis*0.001
axes.plot(ssps.loc[:2020],color='darkblue',linestyle='--')
axes.plot(ssps.iloc[:,1].loc[:2020],color='darkblue',linestyle='--',label='SSPs')

#EDGAR
file = 'EDGAR/EDGAR_v50_CH4_1970_2015.txt'
data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=0,header=0)
data_emis.index.name = 'Year'
edgar5 = data_emis*0.001
print(edgar5)
axes.plot(edgar5,color='lightsalmon',label='EDGARv5')

file = 'EDGAR/EDGAR_v70_FT2021_CH4_1970_2021.txt'
data_emis = pd.read_csv(filepath+file,delimiter=',',index_col=0,header=0)
data_emis.index.name = 'Year'
edgar7 = data_emis*0.001
print(edgar7)
axes.plot(edgar7,color='indianred',label='EDGARv7')


edgar_v50 = pd.DataFrame(data=edgar5.values,index=edgar5.index,columns=['EDGARv5'])
edgar_v70 = pd.DataFrame(data=edgar7.values,index=edgar7.index,columns=['EDGARv7'])
edgar = pd.concat([edgar_v50,edgar_v70],axis=1)

asym_err =np.ones((2,1))
meanv=edgar['EDGARv7'].loc[2018]
maxv=meanv*1.30
minv=meanv*(1.0-0.30)
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

axes.errorbar(2018,meanv , yerr=asym_err, fmt='none',ecolor='salmon',elinewidth=1.5, label='Minx et al. (2021)')

asym_err =np.ones((2,1))
meanv=edgar['EDGARv5'].loc[2015]
maxv=meanv*1.46
minv=meanv*(1.0-0.33)
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

#From excel sheet in the supplementary of Hogh-Isakson
file = 'GAINSv4.txt'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=0)
data_emis.index.name = 'Year'
print(data_emis)

gains_v4  = data_emis
axes.plot(gains_v4,color='violet',label='GAINSv4')





#GMB ranges
#;From table 3, GMB 2020
#;Antropogenic sources:
#;Sum the mean values for bottom up 2017 values.
#;And sum the min and max
#;Agr and waste + fossil fuel + biofuel: 213+135+13 
#;Min: 198+121+10
#;Max: 232+164+14

asym_err =np.ones((2,1))
meanv=213+135+13  
maxv=232+164+14
minv=198+121+10
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

axes.errorbar(2017-0.5,meanv , yerr=asym_err, fmt='none',ecolor='k',elinewidth=1.5,label='GMB (Bottom-up)' )

#2000 to 2009 range
#;Agr and waste + fossil fuel + biofuel:
#Mean: 192 +110+12
#Min: 178 + 94 + 9
#Max: 206 + 129 + 14
asym_err =np.ones((2,1))
meanv=  192 +110+12
maxv=206 + 129 + 14
minv=178 + 94 + 9
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

axes.errorbar((2000+2009)/2.0-0.5 ,meanv , yerr=asym_err, fmt='none',ecolor='k',elinewidth=1.5)

######################
#;And sum the min and max
#;Agr and waste + fossil fuel + biofuel: 227+108+13 
#;Min: 205+91+10
#;Max: 246+121+14

asym_err =np.ones((2,1))
meanv=364
maxv=340
minv=381
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

axes.errorbar(2017+0.5,meanv , yerr=asym_err, fmt='none',ecolor='darkgray',elinewidth=1.5,label='GMB (Top-down)' )

#2000 to 2009 range
#;Agr and waste + fossil fuel + biofuel:
#Mean: 192 +110+12
#Min: 178 + 94 + 9
#Max: 206 + 129 + 14
asym_err =np.ones((2,1))
meanv=  332
maxv=312
minv=347
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

axes.errorbar((2000+2009)/2.0+0.5 ,meanv , yerr=asym_err, fmt='none',ecolor='darkgray',elinewidth=1.5)

###############################

#Read and plot emissions
file = '/div/qbo/utrics/OsloCTM3/plot/emissions_csv/emis_biomassburning_CH4_CMIP6.csv'
data_emis = pd.read_csv(file,delimiter=',',index_col=0,header=1)
data_emis.index.name = 'Year'
print(data_emis)
cmip6bb = data_emis
cmip6bb.columns = ["CMIP6BB"]
print(cmip6bb.loc[1951:1996])

axes.plot(cmip6bb,'--',color='darkgreen',label='CMIP6-BB')
print(data_emis)

#GFED
file = 'gfed_v41s.csv'
data_emis = pd.read_csv(filepath+file,delimiter=';',index_col=0,header=1)
data_emis.index.name = 'Year'
print(data_emis)
gfed  = data_emis['GFED_v41s']*0.001 
axes.plot(gfed,color='green',label='GFEDv4.1s')

axes.axvspan(2000, 2007, alpha=0.2, color='lightgray')

axes.set_ylabel("Methane emissions [Tg yr$^{-1}$]")
axes.set_ylim([0,500]) 
axes.set_xlim([1970,2021])

axes.legend(ncol=2,frameon=False,loc='best', bbox_to_anchor=(0.1, 0.1))


#*********************************************************

#Chose these and write to file, for box modeling:
#RCPhistorical+RCP8.5
#RCPhistorical+ECLIPSE_v6
#CEDS_v2017+SSPmid
#EDGAR_V6 (2018=2019=2020)
#CEDS_v2021 (2019=2020)

#Years to use:
year = np.arange(1950,2021)
print(year)

#RCPhistorical+RCP8.5
print(ipcc['RCP'].loc[1950:1990])
hist = ipcc['RCP'].loc[1950:1990]
hist.columns = ["emis"]

print(rcps['RCP8.5'].loc[2000:2020])
fut = rcps['RCP8.5'].loc[2000:2020]
fut.columns = ["emis"]

rcp_hist_rcp85 = pd.concat([hist,fut])
print(rcp_hist_rcp85)

#Interpolate
emissions_rcp85 = np.interp(year,rcp_hist_rcp85.index, rcp_hist_rcp85.values)
print(emissions_rcp85)


#CEDS_v2017+SSPmid

hist=ceds_17['Emis'].loc[1950:2014]
hist.columns = ["emis"]
fut =ssps['REMIND-MAGPIE - SSP5-34-OS'].loc[2015:2020]
fut.columns = ["emis"]
ceds_v17_ssp = pd.concat([hist,fut])
emissions_ceds_v17_ssp = np.interp(year,ceds_v17_ssp.index, ceds_v17_ssp.values)

#CEDS17+GAINS
hist=ceds_17.loc[1950:1989]
hist.columns = ["emis"]
fut = gains_v4
fut.columns = ["emis"]
scale_val = fut['emis'].loc[1990]/ceds_17['Emis'].loc[1990]

gains_ceds17 = pd.concat([hist*scale_val,fut])
print(year)
print(gains_ceds17)

emissions_gains_cedsv17 = np.interp(year,gains_ceds17.index, gains_ceds17['emis'].values)

#CEDS21+GAINS
hist_pre=ceds_17.loc[1950:1969]
hist_pre.columns = ["emis"]

hist=ceds_21.loc[1970:1989]
hist.columns = ["emis"]
scale_val_pre = hist['emis'].loc[1970]/ceds_17.loc[1970]
print(scale_val_pre.values)
hist = pd.concat([hist_pre*scale_val_pre.values,hist])


fut = gains_v4
fut.columns = ["emis"]
scale_val = fut['emis'].loc[1990]/ceds_21['Emis'].loc[1990]

gains_ceds21 = pd.concat([hist*scale_val,fut])
print(year)
print(gains_ceds21)

emissions_gains_cedsv21 = np.interp(year,gains_ceds21.index, gains_ceds21['emis'].values)



hist=edgar['EDGARv7']
print(hist)
hist_pre=ceds_17['Emis'].loc[1950:hist.index[0]]
scale = (hist.iloc[0]/hist_pre[-1:])
hist_pre  = hist_pre*scale.values
hist_pre_int = np.interp(np.arange(1950,hist.index[0]+1),hist_pre.index,hist_pre.values)
print(hist_pre_int)
                         

emissions_edgar_v7 = hist.loc[:2020] #hist.replace(np.nan, edgar['EDGARv6'].loc[2018]).values
emissions_edgar_v7 = np.append(hist_pre_int[0:-1],emissions_edgar_v7)


print(emissions_edgar_v7)


#CEDS_v2021 (2019=2020)
hist=ceds['CEDS_v2021']
print(hist)
hist_pre=ceds_17['Emis'].loc[1950:hist.index[0]]
scale = (hist.iloc[0]/hist_pre[-1:])
hist_pre  = hist_pre*scale.values
hist_pre_int = np.interp(np.arange(1950,hist.index[0]+1),hist_pre.index,hist_pre.values)
print(hist_pre_int)

emissions_ceds_v2021 = hist.replace(np.nan, ceds['CEDS_v2021'].loc[2019]).values
emissions_ceds_v2021 = np.append(hist_pre_int[0:-1],emissions_ceds_v2021)


#************* CEDS_v2021
##CEDS_v2021+ECLIPSE_v6
##Scale hist CEDS to match ECLIPSE_v6 in 1990
#print(ceds['CEDS_v2021'].loc[1970:1989])
#hist = ceds['CEDS_v2021'].loc[1970:1989]
#hist.columns = ["emis"]
#scale_val = eclipse_v6['ECLIPSEv6'].loc[1990]/ceds['CEDS_v2021'].loc[1990]
#print(scale_val)

#hist_pre=ceds_17['Emis'].loc[1950:hist.index[0]]
#scale = (hist.iloc[0]/hist_pre[-1:])
#hist_pre  = hist_pre*scale.values
#hist_pre_int = np.interp(np.arange(1950,hist.index[0]+1),hist_pre.index,hist_pre.values)
#
#print(eclipse_v6['ECLIPSEv6'].loc[1990:2020])
#fut = eclipse_v6['ECLIPSEv6'].loc[1990:2020]
#fut.columns = ["emis"]

#ceds_v2021_eclipse_v6= pd.concat([hist*scale_val,fut])



#********
#GFED:
print(gfed.values)

print(cmip6bb['CMIP6BB'].loc[1950:1996])

gfed_add = cmip6bb['CMIP6BB'].loc[1951:1996] #np.mean(gfed)

print(gfed_add)

emissions_gfed  = np.append(gfed_add,gfed.values)

print(emissions_gfed.size)
print(year.size)

###

column_name = ['rcp_hist_85','ceds_v2017_gains_v4',
               'ceds_v2021_gains_v4','ceds_v17_ssp',
               'edgar_v7','ceds_v2021','GFEDv41s']
column_name_short = {'rcp_hist_85':'RCP',
                     'ceds_v2017_gains_v4':'GAINSv4 ceds17',
                     'ceds_v2021_gains_v4':'GAINSv4',
                     'ceds_v17_ssp': 'CEDS-2017',
                     'edgar_v7': 'EDGARv7',
                     'ceds_v2021':'CEDS-2021',
                     'GFEDv41s':'GFEDv41s'}

colorlist_antr = ['gray','violet','darkblue','indianred','lightblue']

plt.savefig('figures/' + "figure2.png")

fig2, axes2 = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(12,8))
axes2.plot(year,emissions_rcp85,label=column_name_short[column_name[0]], color=colorlist_antr[0])

axes2.plot(year,emissions_gains_cedsv21,label=column_name_short[column_name[2]], color=colorlist_antr[1])
axes2.plot(year,emissions_ceds_v17_ssp,label=column_name_short[column_name[3]], color=colorlist_antr[2])
axes2.plot(year,emissions_edgar_v7,label=column_name_short[column_name[4]], color=colorlist_antr[3])
axes2.plot(year,emissions_ceds_v2021,label=column_name_short[column_name[5]], color=colorlist_antr[4])


axes2.legend()
axes2.axvspan(2000, 2007, alpha=0.2, color='lightgray')

axes2.set_ylabel("Methane emissions [Tg yr$^{-1}$]")
axes2.set_ylim([0,450]) 
axes2.set_xlim([1950,2021])

emissions_gfed = np.append(0,emissions_gfed)
print(emissions_gfed)



#Write to file

emission_out = np.column_stack((emissions_rcp85,
                                emissions_gains_cedsv17,
                                emissions_gains_cedsv21,
                                emissions_ceds_v17_ssp,
                                emissions_edgar_v7,
                                emissions_ceds_v2021,
                                emissions_gfed))



filename = 'INPUT/anthropogenic_emissions_v2_gfed.txt'
df = pd.DataFrame(emission_out,columns=column_name,index=year)
df.index.name = 'Year'
print(df)

#df.to_csv(filename)

plt.savefig('figures/' + "supplementary_figure_1.png")


exit()

