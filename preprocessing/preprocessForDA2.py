import pandas as pd
import numpy as np
import random
from datetime import datetime

old_data = pd.read_csv('data_700.csv',header=0, sep=",",quoting=3,skipinitialspace=True,error_bad_lines=False)

time_old = old_data["datetime"]
co_old = old_data["Carbon Monoxide"]
pm_old = old_data["PM 2.5"]
humidity_old = old_data["humidity"]
temperature_old = old_data["temperature"]
lat_long_data = pd.read_csv('lat_long_data.csv',header=0, sep=",",quoting=3,skipinitialspace=True,error_bad_lines=False)
lat_range = lat_long_data["lat"]
long_range = lat_long_data["long"]
geo_len = len(lat_range)

datetime_new = []
co_new = []
pm_new = []
humidity_new = []
temperature_new = []
latitude_new = []
longitude_new = []

for time in time_old:
	time_list = time.split(" ")
	datetime_obj = time_list[0]+" "+time_list[1]
	datetime_new.append(datetime_obj)

co_new = co_old
pm_new = pm_old
humidity_new = humidity_old
temperature_new = temperature_old

for i in range(len(time_old)):
	latitude_new.append(lat_range[i%geo_len])
	longitude_new.append(long_range[i%geo_len]) 


output = pd.DataFrame( data={"datetime":datetime_new,"field1":co_new,"field2":pm_new,"field3":humidity_new,"field4":temperature_new,"field5":latitude_new,"field6":longitude_new} )  
output.to_csv("upload_data_700.csv",sep=',',quoting=3,index=False)