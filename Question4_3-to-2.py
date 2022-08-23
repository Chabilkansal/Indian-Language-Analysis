#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# Reading the percent-india csv which contains percentage of monolingual,bilingual and trilingual population of each state
df = pd.read_csv('Results/percent-india.csv')
df


# In[3]:


df['Tri_to_Bi'] = df['percent-three'] / df['percent-two']
df


# In[4]:


result_df = pd.DataFrame()


# In[5]:


# Finding the top 3 states with highest ratio of percent trilingual and bilingual people
result_df = df.nlargest(3, ['Tri_to_Bi'])[['state-code','Tri_to_Bi']]
result_df


# In[6]:


# Finding the top 3 states with lowest ratio of percent trilingual and bilingual people and concating it to previous result
result_df = pd.concat([result_df, df.nsmallest(3, ['Tri_to_Bi'])[['state-code','Tri_to_Bi']]])
result_df


# In[7]:


result_df = result_df.drop(['Tri_to_Bi'],axis=1)
result_df.columns = ['state/ut']
result_df.to_csv('Results/3-to-2-ratio.csv',index=None)

