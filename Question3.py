#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from scipy import stats


# In[2]:


df = pd.read_excel('DDW-C18-0000.xlsx')
df


# In[3]:


df.head(10)


# In[4]:


df2 = df.iloc[5:,:]
df2.head(10)


# In[5]:


df2.columns = ['State','District','Area','Region','Age_Group','Sec_Lang_Tot','Sec_Lang_M','Sec_Lang_F','Third_Lang_Tot','Third_Lang_M','Third_Lang_F']
df2


# In[6]:


df2.reset_index(drop = True, inplace = True)
df2


# In[7]:


df2 = df2.drop(['District'], axis= 1 )
df2


# In[8]:


for i in range(4,10):
    df2.iloc[:,i] = pd.to_numeric(df2.iloc[:,i])


# In[9]:


result_df = pd.DataFrame()

result_df['Area'] = df2['Area'].unique()
result_df


# In[10]:


pop_df = pd.read_excel('DDW_PCA0000_2011_Indiastatedist.xlsx')
pop_df


# In[11]:


result_df['rural-tri'] = np.nan
result_df['urban-tri'] = np.nan
result_df['rural-bi'] = np.nan
result_df['urban-bi'] = np.nan
result_df['rural-mono'] = np.nan
result_df['urban-mono'] = np.nan
result_df['rural-pop'] = np.nan
result_df['urban-pop'] = np.nan


# In[12]:


# Calculating the rural/urban Trilingual,bilingual,monolingual and population 
for i in result_df.index:
    rural_pop= pop_df[(pop_df['Name'].str.upper() == result_df.iloc[i,0].upper()) & (pop_df['TRU'] == 'Rural')].iloc[0]['TOT_P']
    urban_pop = pop_df[(pop_df['Name'].str.upper() == result_df.iloc[i,0].upper()) & (pop_df['TRU'] == 'Urban')].iloc[0]['TOT_P']
    rural_third = df2[(df2['Area'].str.upper() == result_df.iloc[i,0].upper()) & (df2['Region'] == 'Rural')].iloc[0]['Third_Lang_Tot']
    urban_third = df2[(df2['Area'].str.upper() == result_df.iloc[i,0].upper()) & (df2['Region'] == 'Urban')].iloc[0]['Third_Lang_Tot']
    rural_sec = df2[(df2['Area'].str.upper() == result_df.iloc[i,0].upper()) & (df2['Region'] == 'Rural')].iloc[0]['Sec_Lang_Tot']
    urban_sec = df2[(df2['Area'].str.upper() == result_df.iloc[i,0].upper()) & (df2['Region'] == 'Urban')].iloc[0]['Sec_Lang_Tot']
   


    result_df.iloc[i,1] = rural_third
    result_df.iloc[i,2] = urban_third
    result_df.iloc[i,3] = rural_sec - rural_third
    result_df.iloc[i,4] = urban_sec - urban_third
    result_df.iloc[i,5] = rural_pop - rural_sec
    result_df.iloc[i,6] = urban_pop - urban_sec
    result_df.iloc[i,7] = rural_pop
    result_df.iloc[i,8] = urban_pop
    
    
result_df


# In[13]:


result_df['p-value'] = np.nan
# Calculating the ratio of trilingual,bilingual and monolingual urban people to rural people
result_df['Third_Lang_Ratio'] = result_df['urban-tri'] / result_df['rural-tri']
result_df['Sec_Lang_Ratio'] = result_df['urban-bi'] / result_df['rural-bi']
result_df['First_Lang_Ratio'] = result_df['urban-mono'] / result_df['rural-mono']
# Calculating the ratio of urban population to rural population
result_df['Pop_Ratio'] = result_df['urban-pop'] / result_df['rural-pop']

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
result_df_tri = result_df[['Area','urban-tri', 'rural-tri', 'urban-pop', 'rural-pop', 'p-value',]]

result_df_tri['urban-percentage'] = (result_df_tri['urban-tri'] / result_df_tri['urban-pop']) * 100
result_df_tri['rural-percentage'] = (result_df_tri['rural-tri'] / result_df_tri['rural-pop']) * 100

result_df_tri = result_df_tri[['Area','urban-percentage','rural-percentage','p-value']]
result_df_tri

result_df_tri.columns = ['state/ut','urban-percentage','rural-percentage','p-value']
result_df_tri.to_csv('Results/geography-india-c.csv',index=None)


# In[15]:


#Storing the results for bilingual percentage
result_df_bi = result_df[['Area','urban-bi', 'rural-bi', 'urban-pop', 'rural-pop', 'p-value',]]

result_df_bi['urban-percentage'] = (result_df_bi['urban-bi'] / result_df_bi['urban-pop']) * 100
result_df_bi['rural-percentage'] = (result_df_bi['rural-bi'] / result_df_bi['rural-pop']) * 100

result_df_bi = result_df_bi[['Area','urban-percentage','rural-percentage','p-value']]
result_df_bi

result_df_bi.columns = ['state/ut','urban-percentage','rural-percentage','p-value']
result_df_bi.to_csv('Results/geography-india-b.csv',index=None)


# In[16]:


#Storing the results for monolingual percentage
result_df_mono = result_df[['Area','urban-mono', 'rural-mono', 'urban-pop', 'rural-pop', 'p-value',]]

result_df_mono['urban-percentage'] = (result_df_mono['urban-mono'] / result_df_mono['urban-pop']) * 100
result_df_mono['rural-percentage'] = (result_df_mono['rural-mono'] / result_df_mono['rural-pop']) * 100

result_df_mono = result_df_mono[['Area','urban-percentage','rural-percentage','p-value']]
result_df_mono

result_df_mono.columns = ['state/ut','urban-percentage','rural-percentage','p-value']
result_df_mono.to_csv('Results/geography-india-a.csv',index=None)

