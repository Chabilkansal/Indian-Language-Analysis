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


df['Bi_to_Mono'] = df['percent-two'] / df['percent-one'] 
df


# In[4]:


# Finding the top 3 states with highest ratio of percent  bilingual and monolingual people
result_df = df.nlargest(3, ['Bi_to_Mono'])[['state-code','Bi_to_Mono']]
result_df


# In[5]:


# Finding the top 3 states with lowest ratio of percent bilingual and monolingual people and concating it to previous result
result_df = pd.concat([result_df, df.nsmallest(3, ['Bi_to_Mono'])[['state-code','Bi_to_Mono']]])
result_df


# In[6]:


result_df = result_df.drop(['Bi_to_Mono'],axis=1)
result_df.columns = ['state/ut']
result_df.to_csv('Results/2-to-1-ratio.csv',index=None)

