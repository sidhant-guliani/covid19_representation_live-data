"""
Function: covid_plot

Example:
input is dictionary fo rconfirmed_case, death_case, recovered_case
covid_plot(countries_list, confirmed_case, death_case, recovered_case)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 10, 5

def covid_plot(countries_list, confirmed_case, death_case, recovered_case):
    for country in countries_list:
        plt.figure()
        dates_count_conf = confirmed_case[country].index.values
        plt.semilogy(dates_count_conf, np.array(confirmed_case[country].Cases.values), c= 'r', label = 'confirmed')
        plt.semilogy(dates_count_conf, np.array(confirmed_case[country].Cases.values), 'ro')

        dates_count_death = death_case[country].index.values
        plt.semilogy(dates_count_death, np.array(death_case[country].Cases.values), c='k', label = 'death')
        plt.semilogy(dates_count_death, np.array(death_case[country].Cases.values), 'ko')

        dates_count_recov = recovered_case[country].index.values
        plt.semilogy(dates_count_recov, np.array(recovered_case[country].Cases.values), 'b', label = 'recovered')
        plt.semilogy(dates_count_recov, np.array(recovered_case[country].Cases.values), 'bo')

        plt.legend(fontsize=15)
        plt.tick_params(rotation= 45, labelsize=15)
        plt.title(country, fontsize=25)
        plt.ylabel('COUNT', fontsize=15)
        plt.xlabel('TIME', fontsize=15)
        plt.grid()
    return (plt.show())
