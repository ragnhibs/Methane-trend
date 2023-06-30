import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import gridspec
import pandas as pd

plt.rcParams['figure.dpi'] = 300
plt.rcParams.update({'errorbar.capsize': 5})
plt.rcParams['font.size'] = 16

#Width for the patches.
width = 0.08

#Liste med filnavn
#path = '/div/amoc/ragnhibs/ICOS/Python/ASCII/'
path = 'ASCII/'

files_swamps = ['tot_wetlandCH4_use_swamps_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2_2000_2017.txt',
                'tot_wetlandCH4_use_swamps_oldGMBCNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2_2000_2012.txt']
labellist_swamps = ["WAD2M","SWAMPS-GLWD"]
colorlist_swamps = ['orangered','darkblue']


files_met = ['tot_wetlandCH4_CNTRv5_I2000Clm50BgcCrop_f09_g16_VER2_1990_2014.txt',
             'tot_wetlandCH4_CNTRv5_I2000Clm50BgcCropCru_f09_g16_VER2_1990_2016.txt',
             'tot_wetlandCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2_1990_2019.txt',]
labellist_met =["GSWP3",
                "CRUNCEP",
                "CRUJRA",]
colorlist_met = ['darkblue','forestgreen','mediumvioletred']

files = ['tot_wetlandCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2_1990_2019.txt',
         'tot_wetlandCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_1990_2019.txt',
         'tot_wetlandCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min_1990_2019.txt',
         'tot_wetlandCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max_1990_2019.txt',
         'tot_wetlandCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max_1990_2019.txt']
labellist =["CRUJRA (baseline)",
            "fch4max",
            "q10ch4min",
            "q10ch4max",
            "fch4max q10ch4max"]
colorlist = ['mediumvioletred',
             'darkviolet',
             'peru',
             'deeppink',
             'yellowgreen',
             'green',
             'green']


plt.figure(figsize=(15, 7))
gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1]) 
ax0 = plt.subplot(gs[0])


#Met-files:
for i in range(len(files_met)):
    #Emty item for getting legend subtitle
    if i == 0 : 
        rect = plt.Rectangle((0, 0.01), 0.01, 0.01,
                             facecolor='white', alpha=0,label='Met.data:')
        ax0.add_patch(rect)


    x0add = 0.0
    filename = files_met[i]
    data = pd.read_csv(path+filename,index_col=0)
    
    #Select the years to be used in the plot NBNB not data for the entire period all scen
    data = data.loc[2008:2017]
 
    #Get the values for the global emissions and regional emissions
    glob =  data.glob
    trop = data.lat_90s30n  
    temp = data.lat_3060n
    north = data.lat_n60
    
    #Plot the dots on the plot:
    x0 = 0.9+x0add
    y0 = min(glob)
    height = max(glob)-min(glob)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_met[i], alpha=1,label=labellist_met[i])
    ax0.add_patch(rect)

    x0 = 1.9+x0add
    y0 = min(trop)
    height = max(trop)-min(trop)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_met[i], alpha=1)
    ax0.add_patch(rect)

    x0 = 2.9+x0add
    y0 = min(temp)
    height = max(temp)-min(temp)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_met[i], alpha=1)
    ax0.add_patch(rect)

    x0 = 3.9+x0add
    y0 = min(north)
    height = max(north)-min(north)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_met[i], alpha=1)
    ax0.add_patch(rect)

#################################################
#Parameter:
for i in range(len(files)):
    if i == 0 : 
        rect = plt.Rectangle((0, 0.01), 0.01, 0.01,
                             facecolor='white', alpha=0,label='Parameter range:')
        ax0.add_patch(rect)
    
    x0add = 0.1
    filename = files[i]
    data = pd.read_csv(path+filename,index_col=0)
    
    #Select the years to be used in the plot
    data = data.loc[2008:2017]
 
    #Get the values for the global emissions and regional emissions
    glob =  data.glob
    trop = data.lat_90s30n  
    temp = data.lat_3060n
    north = data.lat_n60
    
    #Plot the dots on the plot:
    x0 = 0.9+x0add
    y0 = min(glob)
    height = max(glob)-min(glob)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i], alpha=1,label=labellist[i])
    ax0.add_patch(rect)

    x0 = 1.9+x0add
    y0 = min(trop)
    height = max(trop)-min(trop)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i], alpha=1)
    ax0.add_patch(rect)

    x0 = 2.9+x0add
    y0 = min(temp)
    height = max(temp)-min(temp)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i], alpha=1)
    ax0.add_patch(rect)

    x0 = 3.9+x0add
    y0 = min(north)
    height = max(north)-min(north)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i], alpha=1)
    ax0.add_patch(rect)

for i in range(len(files_swamps)):
    if i == 0 : 
        rect = plt.Rectangle((0, 0.01), 0.01, 0.01,
                             facecolor='white', alpha=0,label='Wetland distribution:')
        ax0.add_patch(rect)
        
    x0add = 0.2 
    filename = files_swamps[i]
    
    data = pd.read_csv(path+filename,index_col=0)
    
    #Select the years to be used in the plot
    
    data = data.loc[2008:2017]
 
    #Get the values for the global emissions and regional emissions
    glob =  data.glob
    trop = data.lat_90s30n  
    temp = data.lat_3060n
    north = data.lat_n60
    
    #Plot the dots on the plot:
    x0 = 0.9+x0add
    
    y0 = min(glob)
    height = max(glob)-min(glob)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_swamps[i], alpha=1,label=labellist_swamps[i])
    ax0.add_patch(rect)

    x0 = 1.9+x0add
    y0 = min(trop)
    height = max(trop)-min(trop)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_swamps[i], alpha=1)
    ax0.add_patch(rect)

    x0 = 2.9+x0add
    y0 = min(temp)
    height = max(temp)-min(temp)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_swamps[i], alpha=1)
    ax0.add_patch(rect)

    x0 = 3.9+x0add
    y0 = min(north)
    height = max(north)-min(north)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_swamps[i], alpha=1)
    ax0.add_patch(rect)


#################################################

#Error bar global methane budget
#Bottom-up: 149 [102-182]
#149-102,182-149
asym_err =np.ones((2,1))
asym_err[0,0] = 149-102    #Lower
asym_err[1,0] = 182-149   #Upper
plt.errorbar(0.75,149 , yerr=asym_err, fmt='none',ecolor='k',elinewidth=1.5,label='GMB 2008-2017 (Bottom-up)')

#Top down: 181 [159-200]
asym_err[0,0] = 181-159    #Lower
asym_err[1,0] = 200-181
plt.errorbar(0.80,181 , yerr=asym_err, fmt='none',ecolor='gray',elinewidth=1.5,label='GMB 2008-2017 (Top-down)')

#<30°N	
#115.6	
#146.3	
#70.8	
asym_err[0,0] = 115.6-70.8   #Lower
asym_err[1,0] = 146.3-115.6
plt.errorbar(1.75,115.6 , yerr=asym_err, fmt='none',ecolor='k',elinewidth=1.5)

#Top down:
#<30°N
meanv=139.7
maxv=162.3
minv=116.4
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv
plt.errorbar(1.80,meanv , yerr=asym_err, fmt='none',ecolor='gray',elinewidth=1.5)


#30°N-60°N	
meanv = 24.6
maxv = 42.7
minv = 10.5
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv
plt.errorbar(2.75,meanv , yerr=asym_err, fmt='none',ecolor='k',elinewidth=1.5)

#Top down:
#30°N-60°N
meanv=31.0
maxv=48.4
minv=18.2
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv
plt.errorbar(2.80,meanv , yerr=asym_err, fmt='none',ecolor='gray',elinewidth=1.5)




#60°N-90°N
meanv = 8.6
maxv = 17.7
minv= 2.2
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv
plt.errorbar(3.75,meanv, yerr=asym_err, fmt='none',ecolor='k',elinewidth=1.5)

#Top down:
#60°N-90°N
meanv=12.3
maxv=15.9
minv = 7.2

asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv
plt.errorbar(3.80,meanv, yerr=asym_err, fmt='none',ecolor='gray',elinewidth=1.5)



#Plot vertical line and shading
plt.axvline(x=1.5,color='k')
plt.axvspan(0.5, 1.5, alpha=0.5, zorder=0,color='silver')


#Setter inn all legends i oevre venstre hjoernet
leg = plt.legend(loc='upper right',numpoints=1,fontsize=12 )#title='Meteorological data:',numpoints=1) #,frameon=False)
for patch in leg.get_patches():
    patch.set_height(8)
    patch.set_width(10)
    patch.set_x(15)

#Navngir aksene:
plt.ylabel("Methane emission [Tg yr$^{-1}$]")

plt.ylim([0,220])
plt.xlim([0.5,4.5])

#Setter en tittel:
plt.title("(a) Global and regional wetland emissions 2008 to 2017")

tics_vals = range(1,5 ) #6)
plt.xticks(tics_vals,
           ["Global", "90S-30N", "30N-60N", "60N-90N"])

#######################################################################
###############################sink#####################

ax1 = plt.subplot(gs[1])

width = 0.04

path = 'ASCII/' #'/div/amoc/ragnhibs/ICOS/Python/ASCII/'
files = [sub.replace('wetland', 'sink') for sub in files]
files_met = [sub.replace('wetland', 'sink') for sub in files_met]
#files_swamps = [sub.replace('wetland', 'sink') for sub in files_swamps]

for i in range(len(files_met)):
    x0add = 0.0 #(-1)*0.05
    filename = files_met[i]
    
    data = pd.read_csv(path+filename,index_col=0)
    
    #Select the years to be used in the plot
    
    data = data.loc[2008:2017]
 
    #Get the values for the global emissions and regional emissions
    glob =  data.glob

    #Plot the dots on the plot:
    x0 = 0.9+x0add
    y0 = min(glob)
    height = max(glob)-min(glob)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_met[i], alpha=1,label=labellist_met[i])
    ax1.add_patch(rect)


for i in range(len(files)):
    x0add = 0.1
    filename = files[i]
    data = pd.read_csv(path+filename,index_col=0)
    
    #Select the years to be used in the plot
    data = data.loc[2008:2017]
 
    #Get the values for the global emissions and regional emissions
    glob =  data.glob

    x0 = 0.9+x0add
    y0 = min(glob)
    height = max(glob)-min(glob)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i], alpha=1)
    ax1.add_patch(rect)

'''
for i in range(len(files_swamps)):
    x0add = 0.1+0.1
    filename = files_swamps[i]
    data = pd.read_csv(path+filename,index_col=0)
    
    #Select the years to be used in the plot
    data = data.loc[2008:2017]
 
    #Get the values for the global emissions and regional emissions
    glob =  data.glob

    x0 = 0.9+x0add
    y0 = min(glob)
    height = max(glob)-min(glob)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist_swamps[i], alpha=1)
    ax1.add_patch(rect)
'''

asym_err =np.ones((2,1))
meanv=-30
maxv=-11
minv=-49
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

plt.errorbar(0.75,meanv , yerr=asym_err, fmt='none',ecolor='k',elinewidth=1.5,label='GMB 2008-2017 (Bottom-up)' )
meanv=-38
maxv=-27
minv=-45
asym_err[0,0] = meanv-minv   #Lower
asym_err[1,0] = maxv-meanv

plt.errorbar(0.80,meanv , yerr=asym_err, fmt='none',ecolor='gray',elinewidth=1.5,label='GMB 2008-2017 (Top-down)')





#Plot vertical line and shading
plt.axvline(x=1.5,color='k')
plt.axvspan(0.5, 1.5, alpha=0.5, zorder=0, color='silver')


#Setter inn all legends i oevre venstre hjoernet
#plt.legend(loc='lower right',title='Meteorological data:',numpoints=1,frameon=False)
#Navngir aksene:
plt.ylabel("Methane sink [Tg yr$^{-1}$]")

plt.ylim([-50,0])
plt.xlim([0.5,1.5])

#Setter en tittel:
plt.title("(b) Sink 2008 to 2017")

plt.xticks([1],
           ["Global"] )


plt.savefig('figures/' + "figure4.png")
#plt.show()


