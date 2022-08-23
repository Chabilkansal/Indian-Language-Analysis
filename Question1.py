#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


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


# In[9]:


df2 = df2.drop(['District'], axis= 1 )
df2


# In[10]:


for i in range(4,10):
    df2.iloc[:,i] = pd.to_numeric(df2.iloc[:,i])


# In[12]:


df2['Area'].unique()


# In[13]:


# creating a result dataframe to store final result
result_df = pd.DataFrame()


# In[14]:


# Adding states to result df
result_df['state-code'] = df2['Area'].unique()
result_df


# In[15]:


# Reading Population data to find statewise population
pop_df = pd.read_excel('DDW_PCA0000_2011_Indiastatedist.xlsx')
pop_df


# In[16]:


# Adding percent-one,two,three columns to store the precentage of monolingual, bilingual and trilingual population respectively
result_df['percent-one'] = np.nan
result_df['percent-two'] = np.nan
result_df['percent-three'] = np.nan


# In[17]:


result_df


# In[18]:


# Calculating the percent-one,percent-two,percent-three value for India as well as for all States/UTs
for i in result_df.index:
    pop = pop_df[pop_df['Name'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['TOT_P']
    second_lang = df2[df2['Area'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['Sec_Lang_Tot']
    third_lang = df2[df2['Area'].str.upper() == result_df.iloc[i,0].upper()].iloc[0]['Third_Lang_Tot']
    result_df.iloc[i,1] = ((pop - second_lang) / pop)*100
    result_df.iloc[i,2] = ((second_lang - third_lang) / pop)*100
    result_df.iloc[i,3] = ((third_lang) / pop)*100

result_df


# In[19]:


# Storing the result in percent-india.csv inside Results folder
result_df.to_csv('Results/percent-india.csv',index=None)

