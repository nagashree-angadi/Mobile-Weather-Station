import pandas as pd
import numpy as np
import random
from datetime import datetime

old_data = pd.read_csv('cpcb_btm1.csv',header=0, sep=",",quoting=3,skipinitialspace=True,error_bad_lines=False)

date_old = old_data["Date"]
time_old = old_data["Time"]
co_old = old_data["Carbon Monoxide"]
pm_old = old_data["PM 2.5"]
humidity_old = old_data["Humidity"]

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

for date,time in zip(date_old,time_old):
	date_list = date.split("-")
	date_new = date_list[2]+"-"+date_list[1]+"-"+date_list[0]
	datetime_obj = date_new+" "+time
	datetime_new.append(datetime_obj)

co_new = co_old
pm_new = pm_old
humidity_new = humidity_old

for i in range(len(date_old)):
	time = int(time_old[i].split(":")[0])
	if time <= 8 or time >= 18:
		tmptr = random.randrange(23,28)
	else:
		tmptr = random.randrange(30,36)
	temperature_new.append(tmptr)

for i in range(len(date_old)):
	latitude_new.append(lat_range[i%geo_len])
	longitude_new.append(long_range[i%geo_len]) 

output = pd.DataFrame( data={"datetime":datetime_new,"field1":co_new,"field2":pm_new,"field3":humidity_new,"field4":temperature_new,"field5":latitude_new,"field6":longitude_new} )  
output.to_csv("upload_data_btm1.csv",sep=',',quoting=3,index=False)
