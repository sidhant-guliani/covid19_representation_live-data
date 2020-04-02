"""
This is just workign on the file which is till MARCH 31 2020
at times I have to change "inception" to get the good results. 

Example:
predict("Mainland China", "confirm", 30, inception, zoom in start)
(country name, "confirm/death/recover", for how many days you want to predict)

# inception data of the epidemic in each country so the curve fits better. (hit and trial)

we are using sigmond function:
a = sigmoid midpoint
b = curve steepness (logistic growth)
c = max value        
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime, timedelta


data=pd.read_csv("covid_19_data.csv")
data=data.drop('Last Update', axis=1)
data=data.drop("SNo",axis=1)
data=data.rename(columns={"ObservationDate": "date", "Country/Region": "country", "Province/State": "state","Confirmed":"confirm","Deaths": "death","Recovered":"recover"})

def predict(country, stat, future_days, inception, zoom_start):
    
    def sigmoid_func(x, a, b, c):
        return (c / (1 + np.exp(-b*(x-a))))
    
    if country=="South Korea":
        inception = 8
    if country=="US":
        inception = 28
    if country=="Italy":
        inception = 20

    country_data = data[data["country"]==country].iloc[: , [0, 2, 3 ,4, 5]].copy()
    country_graph = country_data.groupby("date")[['confirm', 'death', 'recover']].sum().reset_index()[inception:]
    y = country_graph[stat]
    x = np.arange(len(y))
    print("predicted values")
    
    # fitting the data on the logistic function
    # use either trf or dogbox as we have provided the bounds
    popt_sig, pcov_sig = curve_fit(sigmoid_func, x, y, method='trf', bounds=([12., 0.001, y.min()],[60., 2.5, 10*y.max()]))
    plt.figure(figsize=(16,8))
    plt.axvline(x[-1], linestyle = '--', color = 'k')
    x_m = np.arange(len(y)+future_days)
    y_m = sigmoid_func(x_m, *popt_sig)
    sigma1 =  np.round(np.sqrt(np.diag(pcov_sig)).mean(), 2)
    plt.plot(x_m, y_m, c='r', marker="+", label=" Predicted data, sigma: "+str(np.round(np.sqrt(np.diag(pcov_sig)).mean(), 2)))
    #plt.text(x_m[-1]+.5, y_m[-1], str(int(y_m[-1])), size = 10)
    plt.fill_between(x_m[-future_days:], y_m[-future_days:]+sigma1, y_m[-future_days:]-sigma1, facecolor='red', alpha=0.5)
    plt.plot(x, y, c='k', marker= "o" , label = "Raw data")

    plt.text(x[-1]-.5, y_m[-1], str(country_graph["date"][len(y)+inception-1]), size = 20)
    
    
    plt.xlabel("# Days", size=20)
    plt.ylabel("Total cases", size=20)
    plt.legend(prop={'size': 15})
    plt.title(country+"'s Data", size=15)
    plt.tick_params(labelsize=15)
    plt.xlim(zoom_start, len(y_m)+1)
    return(plt.show())
