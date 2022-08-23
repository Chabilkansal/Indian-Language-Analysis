#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os
from collections import Counter


# In[2]:


''' To find the top 3 mother tongues and top three overall languages in each region, I am using a nested dictionary(d) 
format to store the first language, second language and third language data of each state. 
Dictionary d has state names as its keys, and another dictionary first as its values,
dictionary first has different languages as its keys and a list as its value,
this list contains following data 
[number of people speaking key language as their first language in present state,a dictionary second]
dictionary second has languages as its key and a list as its values
this list contains following data
[number of people speaking key language as their second language in present state,a dictionary third]
and so on

Example:
d contains a key  'UTTARAKHAND'
d['UTTARAKHAND'] contains key 'HINDI '
d['UTTARAKHAND']['HINDI '] contains a list [numeric value, dictionary second]
d['UTTARAKHAND']['HINDI '][0] will give no. of people having hindi as their first language in Uttarakhand
d['UTTARAKHAND']['HINDI '][1] contains a key 'ENGLISH '
d['UTTARAKHAND']['HINDI '][1]['ENGLISH '] contains a list [numeric value, dictionary third]
d['UTTARAKHAND']['HINDI '][1]['ENGLISH '][0] will give no. of people having english as their second language who have 
hindi as their first language in Uttarakhand
d['UTTARAKHAND']['HINDI '][1]['ENGLISH '][1] contains a key 'BENGALI '
d['UTTARAKHAND']['HINDI '][1]['ENGLISH '][1]['BENGALI '] has the a numeric entry as its value, which gives the no. of 
people having bengali as their third language who have english as their second language and hindi as their first language
in Uttarakhand.
'''


d = {}
# Reading a state C-17 csv in every iteraion and adding its data in d
for file in os.listdir('C-17/'):
    df = pd.read_excel('C-17/'+file,sheet_name=0)

    df2 = df.iloc[5:,:]

    df2.columns = ['State_Code','State','First_Lang_Code','First_Lang','First_Lang_P','First_Lang_M','First_Lang_F',
                  'Sec_Lang_Code','Sec_Lang','Sec_Lang_P','Sec_Lang_M','Sec_Lang_F','Third_Lang_Code','Third_Lang',
                   'Third_Lang_P','Third_Lang_M','Third_Lang_F']

    df2.reset_index(inplace=True, drop=True)

    # Adding the current state as key with value nan
    d[df2['State'].unique()[0]] = np.nan

    i = 0
    # creating the first dictionary to store first languges data for current state
    first = {}
    while (i < df2.shape[0]) and (not pd.isnull(df2.loc[i,'First_Lang'])):
        # Storing the no. of people having df2.loc[i,'First_Lang'] as their first language in first dictionary
        first[df2.loc[i,'First_Lang']] = [int(df2.loc[i,'First_Lang_P'])]
        j = i + 1
        # creating the second dictionary to store second languges data for current first language and current state
        second = {}
        while (j < df2.shape[0]) and (not pd.isnull(df2.loc[j,'Sec_Lang'])):
            # Storing the no. of people having df2.loc[i,'Sec_Lang'] as their second language in second dictionary
            second[df2.loc[j,'Sec_Lang']] = [int(df2.loc[j,'Sec_Lang_P'])]
            k = j + 1
            # creating the third dictionary to store third languge data for current first,second language and current state
            third = {}
            while (k < df2.shape[0]) and (not pd.isnull(df2.loc[k,'Third_Lang'])):
                third[df2.loc[k,'Third_Lang']] = int(df2.loc[k,'Third_Lang_P'])
                k = k + 1
            second[df2.loc[j,'Sec_Lang']].append(third)
            j = k
        first[df2.loc[i,'First_Lang']].append(second)
        i = j

    d[df2['State'].unique()[0]] = first


# #### North: JK, Ladakh, PN, HP, HR, UK, Delhi, Chandigarh
# #### West: RJ, GJ, MH, Goa, Dadra & Nagar Haveli, Daman & Diu
# #### Central: MP, UP, CG
# #### East: BH, WB, OR, JH
# #### South: KT, TG, AP, TN, KL, Lakshadweep, Puducherry
# #### North-East: AS, SK, MG, TR, AR, MN, NG, MZ, Andaman & Nicobar

# In[3]:


# As India is divided into different regions in the question so, merge first language data to find top 3 mothertongues of 
# each region
north_list = ['JAMMU & KASHMIR','PUNJAB','HIMACHAL PRADESH','HARYANA','UTTARAKHAND','NCT OF DELHI','CHANDIGARH']
west_list = ['RAJASTHAN','GUJARAT','MAHARASHTRA','GOA','DADRA & NAGAR HAVELI','DAMAN & DIU']
central_list = ['MADHYA PRADESH','UTTAR PRADESH','CHHATTISGARH']
east_list = ['BIHAR','WEST BENGAL','ODISHA','JHARKHAND']
south_list = ['KARNATAKA','ANDHRA PRADESH','TAMIL NADU','KERALA','LAKSHADWEEP','PUDUCHERRY']
north_east_list = ['ASSAM','SIKKIM','MEGHALAYA','TRIPURA','ARUNACHAL PRADESH','NAGALAND',
                   'MANIPUR', 'MIZORAM','ANDAMAN & NICOBAR ISLANDS']

# these dictionaries will contain languages as it keys and number of people having this language as their mother tongue 
# in respective region as their values
north = {}
west = {}
central = {}
east = {}
south ={}
north_east = {}
for lang in d['INDIA'].keys():
    north[lang] = 0
    west[lang] = 0
    central[lang] = 0
    east[lang] = 0
    south[lang] = 0
    north_east[lang] = 0
    for state in north_list:
        try:
            north[lang] += d[state][lang][0]
        except:
            north[lang] += 0
    for state in west_list:
        try:
            west[lang] += d[state][lang][0]
        except:
            west[lang] += 0
    for state in central_list:
        try:
            central[lang] += d[state][lang][0]
        except:
            central[lang] += 0
    for state in east_list:
        try:
            east[lang] += d[state][lang][0]
        except:
            east[lang] += 0
    for state in south_list:
        try:
            south[lang] += d[state][lang][0]
        except:
            south[lang] += 0
    for state in north_east_list:
        try:
            north_east[lang] += d[state][lang][0]
        except:
            north_east[lang] += 0


# In[4]:


# Creating a Dataframe to store the result
result_1 = pd.DataFrame()

result_1['region'] = ['north','west','central','east','south','north_east']
result_1['language_1'] = np.nan
result_1['language_2'] = np.nan
result_1['language_3'] = np.nan
result_1


# In[5]:


# Using Counter to find top3 mothertongues of different regions and adding it to the result_1 dataframe
k = Counter(north)
high = k.most_common(3)
result_1.iloc[0,1] = high[0][0]
result_1.iloc[0,2] = high[1][0]
result_1.iloc[0,3] = high[2][0]
k = Counter(west)
high = k.most_common(3)
result_1.iloc[1,1] = high[0][0]
result_1.iloc[1,2] = high[1][0]
result_1.iloc[1,3] = high[2][0]
k = Counter(central)
high = k.most_common(3)
result_1.iloc[2,1] = high[0][0]
result_1.iloc[2,2] = high[1][0]
result_1.iloc[2,3] = high[2][0]
k = Counter(east)
high = k.most_common(3)
result_1.iloc[3,1] = high[0][0]
result_1.iloc[3,2] = high[1][0]
result_1.iloc[3,3] = high[2][0]
k = Counter(south)
high = k.most_common(3)
result_1.iloc[4,1] = high[0][0]
result_1.iloc[4,2] = high[1][0]
result_1.iloc[4,3] = high[2][0]
k = Counter(north_east)
high = k.most_common(3)
result_1.iloc[5,1] = high[0][0]
result_1.iloc[5,2] = high[1][0]
result_1.iloc[5,3] = high[2][0]
result_1


# In[6]:


result_1.to_csv('Results/region-india-a.csv',index=None)


# ### In 2nd part we have to find the overall top 3 languages spoken in every region

# In[7]:


# Using dictionary d and adding all the speakers of particular language in a region to 
# find the top 3 languages of that region

north = {}
west = {}
central = {}
east = {}
south ={}
north_east = {}
for lang in d['INDIA'].keys():
    north[lang] = 0
    west[lang] = 0
    central[lang] = 0
    east[lang] = 0
    south[lang] = 0
    north_east[lang] = 0
    for state in north_list:
        # Here north[lang] will contain all the people speaking language lang in north region
        # It will contain all speakers of lang whether lang is someone's first, second or third language
        # similar of west[lang],east[lang] etc
        try:
            north[lang] += d[state][lang][0]
        except:
            north[lang] += 0
        for first_lang in d['INDIA'].keys():
            try:
                north[lang] += d[state][first_lang][1][lang][0]
            except:
                north[lang] += 0
        for first_lang in d['INDIA'].keys():
            for sec_lang in d['INDIA'].keys():
                try:
                    north[lang] += d[state][first_lang][1][sec_lang][1][lang]
                except:
                    north[lang] += 0
    for state in west_list:
        try:
            west[lang] += d[state][lang][0]
        except:
            west[lang] += 0
        for first_lang in d['INDIA'].keys():
            try:
                west[lang] += d[state][first_lang][1][lang][0]
            except:
                west[lang] += 0
        for first_lang in d['INDIA'].keys():
            for sec_lang in d['INDIA'].keys():
                try:
                    west[lang] += d[state][first_lang][1][sec_lang][1][lang]
                except:
                    west[lang] += 0
    for state in central_list:
        try:
            central[lang] += d[state][lang][0]
        except:
            central[lang] += 0
        for first_lang in d['INDIA'].keys():
            try:
                central[lang] += d[state][first_lang][1][lang][0]
            except:
                central[lang] += 0
        for first_lang in d['INDIA'].keys():
            for sec_lang in d['INDIA'].keys():
                try:
                    central[lang] += d[state][first_lang][1][sec_lang][1][lang]
                except:
                    central[lang] += 0
    for state in east_list:
        try:
            east[lang] += d[state][lang][0]
        except:
            east[lang] += 0
        for first_lang in d['INDIA'].keys():
            try:
                east[lang] += d[state][first_lang][1][lang][0]
            except:
                east[lang] += 0
        for first_lang in d['INDIA'].keys():
            for sec_lang in d['INDIA'].keys():
                try:
                    east[lang] += d[state][first_lang][1][sec_lang][1][lang]
                except:
                    east[lang] += 0
    for state in south_list:
        try:
            south[lang] += d[state][lang][0]
        except:
            south[lang] += 0
        for first_lang in d['INDIA'].keys():
            try:
                south[lang] += d[state][first_lang][1][lang][0]
            except:
                south[lang] += 0
        for first_lang in d['INDIA'].keys():
            for sec_lang in d['INDIA'].keys():
                try:
                    south[lang] += d[state][first_lang][1][sec_lang][1][lang]
                except:
                    south[lang] += 0
    for state in north_east_list:
        try:
            north_east[lang] += d[state][lang][0]
        except:
            north_east[lang] += 0
        for first_lang in d['INDIA'].keys():
            try:
                north_east[lang] += d[state][first_lang][1][lang][0]
            except:
                north_east[lang] += 0
        for first_lang in d['INDIA'].keys():
            for sec_lang in d['INDIA'].keys():
                try:
                    north_east[lang] += d[state][first_lang][1][sec_lang][1][lang]
                except:
                    north_east[lang] += 0


# In[8]:


result_2 = pd.DataFrame()
result_2['region'] = ['north','west','central','east','south','north_east']
result_2['language_1'] = np.nan
result_2['language_2'] = np.nan
result_2['language_3'] = np.nan
result_2


# In[9]:


k = Counter(north)
high = k.most_common(3)
result_2.iloc[0,1] = high[0][0]
result_2.iloc[0,2] = high[1][0]
result_2.iloc[0,3] = high[2][0]
k = Counter(west)
high = k.most_common(3)
result_2.iloc[1,1] = high[0][0]
result_2.iloc[1,2] = high[1][0]
result_2.iloc[1,3] = high[2][0]
k = Counter(central)
high = k.most_common(3)
result_2.iloc[2,1] = high[0][0]
result_2.iloc[2,2] = high[1][0]
result_2.iloc[2,3] = high[2][0]
k = Counter(east)
high = k.most_common(3)
result_2.iloc[3,1] = high[0][0]
result_2.iloc[3,2] = high[1][0]
result_2.iloc[3,3] = high[2][0]
k = Counter(south)
high = k.most_common(3)
result_2.iloc[4,1] = high[0][0]
result_2.iloc[4,2] = high[1][0]
result_2.iloc[4,3] = high[2][0]
k = Counter(north_east)
high = k.most_common(3)
result_2.iloc[5,1] = high[0][0]
result_2.iloc[5,2] = high[1][0]
result_2.iloc[5,3] = high[2][0]
result_2


# In[10]:


result_2.to_csv('Results/region-india-b.csv',index=None)

