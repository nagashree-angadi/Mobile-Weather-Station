import pandas as pd
import numpy as np
import matplotlib
import warnings
#matplotlib.use('Agg')
#matplotlib.rcParams['backend'] = 'TkAgg'
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA
import mpld3
from mpld3 import plugins


warnings.filterwarnings("ignore")
file = open("D:\College\Project\Final\dataAnalysis\co_output.txt","w") 

rcParams['figure.figsize'] = 10, 5
np.seterr(all='ignore')
def test_stationarity(timeseries):
    
  #Determing rolling statistics
	#rolmean = pd.rolling_mean(timeseries, window=12)
	rolmean = pd.Series(timeseries).rolling(window=12,center=False).mean()
	#rolstd = pd.rolling_std(timeseries, window=12)
	rolstd = pd.Series(timeseries).rolling(window=12,center=False).std()

  #Plot rolling statistics:
	orig = plt.plot(timeseries, color='blue',label='Original')
	mean = plt.plot(rolmean, color='red', label='Rolling Mean')
	std = plt.plot(rolstd, color='black', label = 'Rolling Std')
	plt.legend(loc='best')
	plt.title('Rolling Mean & Standard Deviation')
	plt.savefig("D:\College\Project\Final\images\co"+str(i)+".png")
	#plt.show()
	#mpld3.save_html(plt,"test.html")
	#mpld3.fig_to_html(plt,template_type="simple")
 	#mpld3.show()


  #Perform Dickey-Fuller test:
	print 'Results of Dickey-Fuller Test:'
	dftest = adfuller(timeseries, autolag='AIC')
	dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
	for key,value in dftest[4].items():
		dfoutput['Critical Value (%s)'%key] = value
	print dfoutput
	

i = 0
data = pd.read_csv('D:\College\Project\Final\data\upload_data_kadu1.csv')
#print data.head()
#print '\n Data Types:'
#print data.dtypes
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
data = pd.read_csv('D:\College\Project\Final\data\upload_data_kadu1.csv', parse_dates=['datetime'], index_col='datetime',date_parser=dateparse)
#print data.head()
#print data.index
co_data = data['field1'] 
#print co_data.head(10)
plt.plot(co_data)

test_stationarity(co_data)
i = i+1
co_log = np.log(co_data)
plt.plot(co_log)
moving_avg = pd.Series(co_log).rolling(window=12,center=False).mean()
plt.plot(co_log)
plt.plot(moving_avg, color='red')
co_log_moving_avg_diff = co_log - moving_avg
co_log_moving_avg_diff.head(12)
co_log_moving_avg_diff.dropna(inplace=True)
test_stationarity(co_log_moving_avg_diff)
i = i+1
expwighted_avg = pd.Series(co_log).ewm(halflife=12,ignore_na=True,min_periods=0,adjust=True).mean()
plt.plot(co_log)
plt.plot(expwighted_avg, color='red')
co_log_ewma_diff = co_log - expwighted_avg
test_stationarity(co_log_ewma_diff)
i = i+1
co_log_diff = co_log - co_log.shift()
plt.plot(co_log_diff)
co_log_diff.dropna(inplace=True)
test_stationarity(co_log_diff)
i = i+1

decomposition = seasonal_decompose(co_log, freq=30)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(co_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()

co_log_decompose = residual
co_log_decompose.dropna(inplace=True)
test_stationarity(co_log_decompose)

lag_acf = acf(co_log_diff, nlags=20)
lag_pacf = pacf(co_log_diff, nlags=20, method='ols')

#Plot ACF: 
plt.subplot(121) 
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(co_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(co_log_diff)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')

#Plot PACF:
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(co_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(co_log_diff)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
plt.savefig("D:\College\Project\Final\images\co_Auto.png")
'''
model = ARIMA(co_log, order=(2, 1, 0))  
results_AR = model.fit(disp=-1)  
plt.plot(co_log_diff)
plt.plot(results_AR.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_AR.fittedvalues-co_log_diff)**2))
#plt.show()
#plt.savefig("D:\College\Project\Final\images\coRSSS.png")

model = ARIMA(co_log, order=(0, 1, 2))  
results_MA = model.fit(disp=-1)  
plt.plot(co_log_diff)
plt.plot(results_MA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_MA.fittedvalues-co_log_diff)**2))
plt.show()
#plt.savefig("D:\College\Project\Final\images\coRSS2.png")

model = ARIMA(co_log, order=(2, 1, 2))  
results_ARIMA = model.fit(disp=-1)  
plt.plot(co_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-co_log_diff)**2))

predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
print predictions_ARIMA_diff.head() 

predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
print predictions_ARIMA_diff_cumsum.head()

predictions_ARIMA_log = pd.Series(co_log.ix[0], index=co_log.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
predictions_ARIMA_log.head()

predictions_ARIMA = np.exp(predictions_ARIMA_log)
plt.plot(co_data)
plt.plot(predictions_ARIMA)
plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-co_data)**2)/len(co_data)))'''

file.close();