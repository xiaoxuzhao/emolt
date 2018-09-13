# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:10:05 2018
seasonal daliy catch 
@author: xiaoxu zhao
"""
from datetime import datetime, timedelta
from pandas import Series
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
#from getdata_eric import getobs_temp
from pandas import read_csv
import numpy as np
##########################
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
file='catch_temp_file_BD.csv' # catch data that JiM created &  emailed
#tempfile='BN01_wtmp_dc_36.csv'
input_dir='/home/zdong/xiaoxu/emolt/files/'
catch_colnum=12 # column number where "11' refers to lobster "kept"
date_colnum=6#column number where "11' refers to lobster "date"
haul_number=12.0000
temp_colnum=17
d=5
t='BD01'
#######################
df=read_csv(input_dir+file) # reads catch data
#dfh=read_csv(input_dir+tempfile)
temp=df.icol(temp_colnum)
tcatch=df.icol(catch_colnum)# catch number
date=df.icol(date_colnum)#2000-09-15:08:43
catch = [x/haul_number for x in tcatch]
newdate=[]
for i in range(len(date)):
    newdate.append(datetime.strptime(date[i],"%Y-%m-%d:%H:%M").replace(year=2000))
T=pd.Series(newdate)
####################
daliycatch=[]
ndate=[]
daliytemp=[]
i=0
while i<len(newdate):#len(newdate)
      num=[]
      mean_catch=[]
      mean_temp=[]
      mean_date=[]
      for s in T.index:
         if newdate[i].timetuple().tm_mon==newdate[s].timetuple().tm_mon and newdate[i].timetuple().tm_mday==newdate[s].timetuple().tm_mday :
            num.append(s)
            mean_catch.append(catch[s])
            mean_temp.append(temp[s])
            mean_date.append(newdate[s])
      if len(num)>0:
          daliycatch.append(np.mean(mean_catch))
          daliytemp.append(np.mean(mean_temp))
          ndate.append(mean_date[0])
      else:
          daliycatch.append(catch[i])
          daliytemp.append(temp[i])
          ndate.append(newdate[i])
      for d in num:
            del T[d]
      if len(T)==0:
          break
      else:
          i=T.index[0]
data= {'catch':daliycatch,'temp':daliytemp,'date':ndate}
fig=pd.DataFrame(data)
f=fig.dropna().sort('date')
dat=[(p.month+p.day/30.000) for p in f.date]
########################
fig,ax1=plt.subplots()
ax1.plot(dat,list(f.catch),'-b',linewidth=1)
ax1.set_xlabel('Month',fontsize=10)
ax1.set_ylabel('seasonal catch', color='b')
#ax1.tick_params('y', colors='black')
ax2 = ax1.twinx()
ax2.plot(dat,list(f.temp),'-r',linewidth=1)
ax2.set_ylabel('seasonal temperature', color='r')
#ax2.tick_params('y', colors='black')
ax1.legend(['catch'],loc=2,fontsize=10)
ax2.legend(['temp'],loc=0,fontsize=10)
ax1.set_xlim(0,13)
plt.title('seasonal daliy mean catch vs mean temp at eMOLT site '+t)
plt.savefig(save_dir+"seasonal daliy mean catch and mean temp and date"+t+".png")
plt.show()      