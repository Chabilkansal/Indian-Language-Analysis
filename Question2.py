#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from scipy import stats


# In[2]:


# Reading C-18 POPULATION BY BILINGUALISM, TRILINGUALISM, AGE AND SEX
df = pd.read_excel('DDW-C18-0000.xlsx')
df


# In[3]:


df.head(10)


# In[4]:


# As the data starts from 6 row so removing all previous rows
df2 = df.iloc[5:,:]
df2.head(10)


# In[5]:


# Renaming columns appropriately
df2.columns = ['State','District','Area','Region','Age_Group','Sec_Lang_Tot','Sec_Lang_M','Sec_Lang_F','Third_Lang_Tot','Third_Lang_M','Third_Lang_F']
df2


# In[6]:


df2.reset_index(drop = True, inplace = True)
df2


# In[7]:


df2 = df2.drop(['District'], axis= 1 )
df2


# In[8]:


# Changing the data type of numeric columns 
for i in range(4,10):
    df2.iloc[:,i] = pd.to_numeric(df2.iloc[:,i])


# In[9]:


# creating a result dataframe to store final result
result_df = pd.DataFrame()

# Adding State/UT names to result df
result_df['Area'] = df2['Area'].unique()
result_df


# In[10]:


# Reading Population data to find statewise male/female  population
pop_df = pd.read_excel('DDW_PCA0000_2011_Indiastatedist.xlsx')
pop_df


# In[11]:


# Adding multiple columns to store monolingual,bilingual and trilingual data of male/females in each State/UT also the
# population of males and females in each state
result_df['First_Lang_M'] = np.nan
result_df['First_Lang_F'] = np.nan
result_df['Sec_Lang_M'] = np.nan
result_df['Sec_Lang_F'] = np.nan
result_df['Third_Lang_M'] = np.nan
result_df['Third_Lang_F'] = np.nan
result_df['Pop_M'] = np.nan
result_df['Pop_F'] = np.nan


# In[12]:


# Finding the values of monolingual,bilingual and trilingual males/females in each state using df2  and male/female population
# using pop_df
for i in result_df.index:
    pop_M = pop_df[pop_df['Name'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['TOT_M']
    pop_F = pop_df[pop_df['Name'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['TOT_F']
    sec_lang_M = df2[df2['Area'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['Sec_Lang_M']
    sec_lang_F = df2[df2['Area'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['Sec_Lang_F']    
    third_lang_M = df2[df2['Area'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['Third_Lang_M']
    third_lang_F = df2[df2['Area'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['Third_Lang_F']
    first_lang_M = pop_M - sec_lang_M
    first_lang_F = pop_F - sec_lang_F
    sec_lang_M = sec_lang_M - third_lang_M
    sec_lang_F = sec_lang_F - third_lang_F
    result_df.iloc[i,1] = first_lang_M
    result_df.iloc[i,2] = first_lang_F
    result_df.iloc[i,3] = sec_lang_M
    result_df.iloc[i,4] = sec_lang_F
    result_df.iloc[i,5] = third_lang_M
    result_df.iloc[i,6] = third_lang_F
    result_df.iloc[i,7] = pop_M
    result_df.iloc[i,8] = pop_F

result_df


# In[13]:


result_df['p-value'] = np.nan
# Calculating the ratio of trilingual,bilingual and monolingual males to females
result_df['Third_Lang_Ratio'] = result_df['Third_Lang_M'] / result_df['Third_Lang_F']
result_df['Sec_Lang_Ratio'] = result_df['Sec_Lang_M'] / result_df['Sec_Lang_F']
result_df['First_Lang_Ratio'] = result_df['First_Lang_M'] / result_df['First_Lang_F']
# Calculating the ratio of males to females population
result_df['Pop_Ratio'] = result_df['Pop_M'] / result_df['Pop_F']

for i in result_df.index:
    lang_ratios = []
    lang_ratios.extend([result_df.loc[i,'First_Lang_Ratio'],
                        result_df.loc[i,'Sec_Lang_Ratio'],
                        result_df.loc[i,'Third_Lang_Ratio']])
    
    cur_pop_ratio = result_df.loc[i,'Pop_Ratio']
# Using ttest to find the pval for each state
    _,pval = stats.ttest_1samp(lang_ratios,cur_pop_ratio)
    result_df.loc[i,'p-value'] = pval
result_df


# In[14]:


#Storing the results for trilingual percentage
result_df_tri = result_df[['Area','Third_Lang_M', 'Third_Lang_F', 'Pop_M', 'Pop_F', 'p-value',]]

result_df_tri['male-percentage'] = (result_df_tri['Third_Lang_M'] / result_df_tri['Pop_M']) * 100
result_df_tri['female-percentage'] = (result_df_tri['Third_Lang_F'] / result_df_tri['Pop_F']) * 100

result_df_tri = result_df_tri[['Area','male-percentage','female-percentage','p-value']]
result_df_tri

result_df_tri.columns = ['state/ut','male-percentage','female-percentage','p-value']
result_df_tri.to_csv('Results/gender-india-c.csv',index=None)


# In[15]:


#Storing the results for bilingual percentage
result_df_bi = result_df[['Area','Sec_Lang_M', 'Sec_Lang_F', 'Pop_M', 'Pop_F', 'p-value',]]

result_df_bi['male-percentage'] = (result_df_bi['Sec_Lang_M'] / result_df_bi['Pop_M']) * 100
result_df_bi['female-percentage'] = (result_df_bi['Sec_Lang_F'] / result_df_bi['Pop_F']) * 100

result_df_bi = result_df_bi[['Area','male-percentage','female-percentage','p-value']]
result_df_bi

result_df_bi.columns = ['state/ut','male-percentage','female-percentage','p-value']
result_df_bi.to_csv('Results/gender-india-b.csv',index=None)


# In[16]:


#Storing the results for monolingual percentage
result_df_mono = result_df[['Area','First_Lang_M', 'First_Lang_F', 'Pop_M', 'Pop_F', 'p-value',]]

result_df_mono['male-percentage'] = (result_df_mono['First_Lang_M'] / result_df_mono['Pop_M']) * 100
result_df_mono['female-percentage'] = (result_df_mono['First_Lang_F'] / result_df_mono['Pop_F']) * 100

result_df_mono = result_df_mono[['Area','male-percentage','female-percentage','p-value']]
result_df_mono

result_df_mono.columns = ['state/ut','male-percentage','female-percentage','p-value']
result_df_mono.to_csv('Results/gender-india-a.csv',index=None)

