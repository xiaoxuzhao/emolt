# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 12:10:19 2018
emolt temp vs catch
@author: xiaoxu
"""
import datetime
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import pandas as pd
import numpy as np
from pandas import read_csv
##########################
#HARDCODES
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
file_catch='sqldump_2018_07_BN.csv' # catch data that JiM created &  emailed
input_dir='/home/zdong/xiaoxu/emolt/files/'
file_temp='this2.dat'  #temp data
colnum=11 # column number where "11' refers to lobster "kept"
##########################
df_catch=read_csv(input_dir+file_catch) # reads catch data
catch=df_catch.icol(colnum)# catch number
date=df_catch.icol(5)#2000-09-15:08:43
variables=['year','year_day','temp','lat','lon','depth']
df_temp=pd.read_csv(input_dir+file_temp, names=variables, sep='\s+') # read temperature time series
temp=df_temp["temp"]
tyear=df_temp["year"]
tyear_d=df_temp["year_day"]            

#################
#change catch datetime to year_day
cyear_d=[]
for i in range(0,len(date)):
     day=datetime.datetime.strptime(date[i],"%Y-%m-%d:%H:%M").timetuple().tm_yday  # gets yearday
     cyear_d.append(day)     

#################
# create mean temp 
mean_temp=[]
for s in range(0,len(catch)):
        print s
        Temp=[]
        for i in range(len(temp)): 
           if int(date[s][0:4])==tyear[i] and cyear_d[s]==int(tyear_d[i]):
               #match year and year_day
               Temp.append(temp[i])
        mean_temp.append(np.mean(Temp))#creates mean temperature on the day he hauled
####################
aver_temp=[]
for i in range(len(mean_temp)-1):
    aver_temp.append((mean_temp[i]+mean_temp[i+1])/2)
i=len(mean_temp)-1    
aver_temp.append((mean_temp[i]+mean_temp[0])/2)
####################
fig = plt.figure()
a=fig.add_subplot(1,1,1)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(aver_temp,catch, 'o', marker=cut_star, markersize=15)
plt.ylabel('catch')
plt.xlabel('average_temperature')
plt.savefig(save_dir+"plot_catch_average_temperature.png")
plt.show()