import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import gridspec
import pandas as pd


plt.rcParams.update({'errorbar.capsize': 5})
plt.rcParams['font.size'] = 16

#Width for the patches.
width = 0.08

#Liste med filnavn
path = 'ASCII/' #'/div/amoc/ragnhibs/ICOS/Python/ASCII/'

#Do not add the wetland dist here in the net.
files_swamps = []
labellist_swamps = ["WAD2M","SWAMPS-GLWD"]
colorlist_swamps = ['orangered','darkblue']


files_met = ['totCH4_CNTRv5_I2000Clm50BgcCrop_f09_g16_VER2_1990_2014.txt',
             'totCH4_CNTRv5_I2000Clm50BgcCropCru_f09_g16_VER2_1990_2016.txt',
             'totCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2_1990_2019.txt',]
labellist_met =["GSWP3",
                "CRUNCEP",
                "CRUJRA",]

colorlist_met = ['darkblue','forestgreen','mediumvioletred']

files = ['totCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_VER2_1990_2019.txt',
         'totCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_1990_2019.txt',
         'totCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4min_1990_2019.txt',
         'totCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_q10ch4max_1990_2019.txt',
         'totCH4_CNTRv5_I2000Clm50BgcCropCRUJRA_f09_g16_fch4max_q10ch4max_1990_2019.txt']

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


#plt.figure(figsize=(15, 7))
fig, ax0 = plt.subplots(1,1,figsize=(12,7))


#Met-files:
for i in range(len(files_met)):
    #Emty item for getting legend subtitle
    if i == 0 : 
        rect = plt.Rectangle((0, 0.01), 0.01, 0.01,
                             facecolor='white', alpha=0,label='Met.data:')
        ax0.add_patch(rect)


    x0add = 0.0
    filename = files_met[i]
    print(filename)
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
        
    if i==0:
        zorder = 10
    else:
        zorder = 1

    x0add = 0.1
    filename = files[i]
    print(filename)
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
                                 facecolor=colorlist[i], zorder=zorder, alpha=1,label=labellist[i])
    ax0.add_patch(rect)

    x0 = 1.9+x0add
    y0 = min(trop)
    height = max(trop)-min(trop)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i],  zorder=zorder,alpha=1)
    ax0.add_patch(rect)

    x0 = 2.9+x0add
    y0 = min(temp)
    height = max(temp)-min(temp)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i],  zorder=zorder,alpha=1)
    ax0.add_patch(rect)

    x0 = 3.9+x0add
    y0 = min(north)
    height = max(north)-min(north)
    rect = plt.Rectangle((x0, y0), width, height,
                                 facecolor=colorlist[i],  zorder=zorder,alpha=1)
    ax0.add_patch(rect)

for i in range(len(files_swamps)):
    if i == 0 : 
        rect = plt.Rectangle((0, 0.01), 0.01, 0.01,
                             facecolor='white', alpha=0,label='Wetland distribution:')
        ax0.add_patch(rect)
        
    x0add = 0.2 
    filename = files_swamps[i]
    print(filename)
    data = pd.read_csv(path+filename,index_col=0)
    
    #Select the years to be used in the plot
    
    data = data.loc[2008:2017]
    print(data)
    
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

#Plot vertical line and shading
plt.axvline(x=1.5,color='k')
plt.axvspan(0.5, 1.5, alpha=0.3, zorder=0,color='silver')



leg = plt.legend(loc='upper right',numpoints=1,fontsize=12 )
for patch in leg.get_patches():
    patch.set_height(8)
    patch.set_width(10)
    patch.set_x(15)


plt.ylabel("Methane emissions [Tg yr$^{-1}$]")

plt.ylim([0,250])
plt.xlim([0.5,4.5])


plt.title("Global and regional net emissions 2008 to 2017")

tics_vals = range(1,5)
plt.xticks(tics_vals,
           ["Global", "90S-30N", "30N-60N", "60N-90N"])
plt.show()



#######################################################################
