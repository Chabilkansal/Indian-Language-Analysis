#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# Reading C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX

df = pd.read_excel('DDW-C19-0000.xlsx')
df


# In[3]:


df.head(10)


# In[4]:


df2 = df.iloc[5:,:]
df2.head(10)


# In[5]:


# Renaming Columns appropriately
df2.columns = ['State','District','Area','Region','Education_Level','Sec_Lang_Tot','Sec_Lang_M','Sec_Lang_F','Third_Lang_Tot','Third_Lang_M','Third_Lang_F']
df2


# In[6]:


df2 = df2.iloc[:-3,:]
df2


# In[7]:


df2.reset_index(drop = True, inplace = True)
df2


# In[10]:


# Dropping unnecessary columns
df2 = df2.drop(['District'], axis= 1 )
df2


# In[11]:


# Changing the data type of numerical attributes
for i in range(4,10):
    df2.iloc[:,i] = pd.to_numeric(df2.iloc[:,i])


# In[13]:


df2[(df2['Area'] == 'INDIA') & (df2['Region'] == 'Total')]


# In[14]:


df3 = pd.DataFrame()


# In[15]:


# Creating a dataframe which contains total triligual speakers for each educational level of every Area
for area in df2['Area'].unique():
    temp_df = df2[(df2['Area'].str.upper() == area.upper()) & (df2['Region'].str.upper() == 'TOTAL')].iloc[1:,:]
    temp_df.drop(['State','Region','Sec_Lang_Tot','Sec_Lang_M','Sec_Lang_F','Third_Lang_M','Third_Lang_F'], axis=1, inplace = True)
    df3 = pd.concat([df3, temp_df])
df3


# In[16]:


# Reading C-8 to find the educational level wise population in each state
pop_df = pd.read_excel('DDW-0000C-08.xlsx')
pop_df


# In[17]:


pop_df.head(10)


# In[18]:


# Renaming columns appropriately
pop_df.columns = ['Table_Name','State_Code','District_Code','Area','Region','Age_Group','Total_P','Total_M','Total_F',
                  'Illiterate_P','Illiterate_M','Illiterate_F','Literate_P','Literate_M','Literate_F',
                  'Literate_w/o_education_level_P','Literate_w/o_education_level_M','Literate_w/o_education_level_F','Below_Primary_P',
                  'Below_Primary_M','Below_Primary_F','Primary_P','Primary_M','Primary_F','Middle_P','Middle_M','Middle_F',
                  'Matric_P','Matric_M','Matric_F','Intermediate_P','Intermediate_M','Intermediate_F','NonTechnical_Diploma_P',
                  'NonTechnical_Diploma_M','NonTechnical_Diploma_F','Technical_Diploma_P','Technical_Diploma_M',
                  'Technical_Diploma_F','Graduate_P','Graduate_M','Graduate_F','Unclassified_P','Unclassified_M','Unclassified_F']
pop_df.head(10)


# In[19]:


pop_df = pop_df.iloc[6:,:]
pop_df


# In[20]:


pop_df.reset_index(inplace=True,drop=True)
pop_df


# In[22]:


# As in C-19 csv (df3) some literacy levels are merged with other literacy levels so merge there literacy levels in pop_df too 
pop_df['Literate_P'] = pop_df['Literate_P'] + pop_df['Literate_w/o_education_level_P'] + pop_df['Unclassified_P']
pop_df['Matric_P'] = pop_df['Matric_P'] + pop_df['NonTechnical_Diploma_P'] + pop_df['Technical_Diploma_P'] + pop_df['Intermediate_P']


# In[23]:


pop_df


# In[24]:


pop_df.columns


# In[25]:


# Dropping unnessecary columns
pop_df = pop_df.drop(['Table_Name', 'State_Code', 'District_Code','Total_P','Total_M', 'Total_F','Illiterate_M',
                      'Illiterate_F','Literate_M','Literate_F','Literate_w/o_education_level_P',
                      'Literate_w/o_education_level_M','Literate_w/o_education_level_F','Below_Primary_M','Below_Primary_F',
                     'Primary_M', 'Primary_F','Middle_M', 'Middle_F','Matric_M', 'Matric_F',
                     'Intermediate_P','Intermediate_M','Intermediate_F','NonTechnical_Diploma_P',
                      'NonTechnical_Diploma_M','NonTechnical_Diploma_F', 'Technical_Diploma_P',
                      'Technical_Diploma_M','Technical_Diploma_F','Graduate_M', 'Graduate_F',
                     'Unclassified_P', 'Unclassified_M', 'Unclassified_F'],axis=1)
pop_df


# In[26]:


# Adding population column
df3['Population'] = np.nan

df3


# In[27]:


df3.reset_index(drop=True,inplace=True)
df3


# In[28]:


pop_df


# In[29]:


pop_df[[True if 'ANDAMAN & NICOBAR ISLANDS' in i else False for i in pop_df['Area']]]


# In[30]:


df3.head(20)


# In[31]:


# Finding the population for each educational level from pop_df and adding it to df3
for i in df3.index:
    temp_df = pop_df[[True if df3.iloc[i,0].upper() in area.upper() else False for area in pop_df['Area']]]
    if df3.iloc[i,1] == 'Illiterate':    
        df3.iloc[i,3] = int(temp_df.iloc[0]['Illiterate_P'])
    elif df3.iloc[i,1] == 'Literate':    
        df3.iloc[i,3] = int(temp_df.iloc[0]['Literate_P'])
    elif df3.iloc[i,1] == 'Literate but below primary':    
        df3.iloc[i,3] = int(temp_df.iloc[0]['Below_Primary_P'])
    elif df3.iloc[i,1] == 'Primary but below middle':    
        df3.iloc[i,3] = int(temp_df.iloc[0]['Primary_P'])
    elif df3.iloc[i,1] == 'Middle but below matric/secondary':    
        df3.iloc[i,3] = int(temp_df.iloc[0]['Middle_P'])
    elif df3.iloc[i,1] == 'Matric/Secondary but below graduate':    
        df3.iloc[i,3] = int(temp_df.iloc[0]['Matric_P'])
    elif df3.iloc[i,1] == 'Graduate and above':    
        df3.iloc[i,3] = int(temp_df.iloc[0]['Graduate_P'])
df3


# In[32]:


df3.head(20)


# In[33]:


# Finding the percentage of people trilingual in each educational level of every state
df3['Trilingual (%)'] = (df3['Third_Lang_Tot'] / df3['Population']) * 100
df3


# In[34]:


df4 = df3.drop(['Third_Lang_Tot','Population'],axis=1)
df4


# In[35]:


# Finding the educational level for each state which has maximum percentage of trilingual people
idx = df4.groupby(['Area'])['Trilingual (%)'].transform(max) == df4['Trilingual (%)']
df5 = df4[idx]
df5


# In[36]:


df5.reset_index(drop=True, inplace=True)


# In[37]:


df5


# In[38]:


# Saving the results in literacy-india.csv inside Results directory
df5.columns = ['state/ut','literacy-group','percentage']
df5.to_csv('Results/literacy-india.csv',index=None)

