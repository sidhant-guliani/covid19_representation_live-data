# loading data
# INPUT
"""
Function: load
INPUT
covid_id: string ('confirmed' /death/ recovered)
wanter_countries: array (['Canada', 'India','China', 'US'])
OUTPUT:
df_dict: dictionary

example:
import COVID_load as cl
conf_IND_CHN = cl.load('Confirmed',['India','China'])

Function: countries_list
example:
countries_list()
# NOTE: shows countries list of confirmed cases only
"""

import pandas as pd
import numpy as np
from datetime import datetime,timedelta


confirmed_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
deaths_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
recovered_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

confirmed_fixes_dict = {'Italy|2020-03-12': 15113,
                        'Spain|2020-03-12': 3146,
                        'France|2020-03-12': 2876,
                        'United Kingdom|2020-03-12': 590,
                        'Germany|2020-03-12': 2745,
                        'Argentina|2020-03-12': 19,
                        'Australia|2020-03-12': 122,
                        'Belgium|2020-03-12': 314,
                        'Chile|2020-03-12': 23,
                        'Colombia|2020-03-12': 9,
                        'Greece|2020-03-12': 98,
                        'Indonesia|2020-03-12': 34,
                        'Ireland|2020-03-12': 43,
                        'Japan|2020-03-12': 620,
                        'Netherlands|2020-03-12': 503,
                        'Qatar|2020-03-12': 262,
                        'Singapore|2020-03-12': 178,
                        'France|2020-03-15': 5423,}
                        
deaths_fixes_dict = {'Italy|2020-03-12': 1016,
                     'Spain|2020-03-12': 86,
                     'France|2020-03-12': 61,
                     'United Kingdom|2020-03-12': 10,
                     'Germany|2020-03-12': 6,
                     'Argentina|2020-03-12': 1,
                     'Australia|2020-03-12': 3,
                     'Greece|2020-03-12': 1,
                     'Indonesia|2020-03-12': 1,
                     'Ireland|2020-03-12': 1,
                     'Japan|2020-03-12': 15,
                     'Netherlands|2020-03-12': 5,
                     'Switzerland|2020-03-12': 4,
                     'United Kingdom|2020-03-15': 35,
                     'France|2020-03-15': 127}
                     
recovered_fixes_dict = {'Italy|2020-03-12': 1258,
                        'Spain|2020-03-12': 189,
                        'France|2020-03-12': 12,
                        'Germany|2020-03-12': 25}

def countries_list():
    # note returning countries list in confirmes cases only
    curl = confirmed_data
    corona_cases_df = pd.read_csv(curl)
    country_list = np.unique(corona_cases_df['Country/Region'].values)
    return(country_list)


def load(covid_id, wanted_countries):
    # covid ID 
    if covid_id=='Confirmed':
        curl = confirmed_data
    elif covid_id =='Deaths':
        curl = deaths_data
    elif covid_id =='Recovered':
        curl = recovered_data
    #   use first four columns as multiindex
    corona_cases_df = pd.read_csv(curl, index_col=[0,1,2,3])
    #return (corona_cases_df)
    
    # to check if the countries list you are askign for is in data or not
    country_list = (corona_cases_df.index.get_level_values('Country/Region').values)
    countries_list = [np.unique(np.array([s for s in country_list if cou in s])) for cou in wanted_countries]
    countries_list = np.array(countries_list).flatten()
    
    cases_percountry = {}
    df_dict = {}
    for country in countries_list:

        # CHECK THE INDEX SLICE EXAMPLE ABOVE. WE ARE DOIGN THIS TO GET ALL THE DATA FOR THE COUNTRY WE ARE LOOKING FOR
        # we are doing sum for the total number of cases in a country, eg: in canada we have 12 rows for wach province
        # but we want to see for whole canada
        cou = corona_cases_df.loc[pd.IndexSlice[:, country], :].sum()

        # getting rid of the record which has zero cases
        cases_percountry[country] = cou[cou > 0]
        datesformat = [datetime.strptime(da, '%m/%d/%y') for da in cases_percountry[country].index]
        df_dict[country] = pd.DataFrame(cases_percountry[country], columns=['Cases'], index=datesformat)
        df_dict[country]['DayCount'] = np.arange(1,cases_percountry[country].shape[0]+1)
        
    
    # fixing the data, manually corrected  
    if covid_id=='Confirmed':
        fixes_dict = confirmed_fixes_dict

    elif covid_id =='Deaths':
        fixes_dict = deaths_fixes_dict

    elif covid_id =='Recovered':
        fixes_dict = recovered_fixes_dict   

    for key in fixes_dict.keys():
            country_to_be_fixed = key.split('|')[0]
            if country_to_be_fixed in df_dict.keys():
                date_to_be_fixed = key.split('|')[1]
                value_to_be_fixed = fixes_dict[key]
                df_dict[country_to_be_fixed]['Cases'].loc[date_to_be_fixed] = value_to_be_fixed
                
    return(df_dict)
