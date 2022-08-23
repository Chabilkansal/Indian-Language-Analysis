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


df2 = df.iloc[5:,:]
df2.head(10)


# In[5]:


# Renaming Columns appropriately
df2.columns = ['State','District','Area','Region','Age_Group','Sec_Lang_Tot','Sec_Lang_M','Sec_Lang_F','Third_Lang_Tot','Third_Lang_M','Third_Lang_F']
df2


# In[6]:


df2.reset_index(drop = True, inplace = True)
df2


# In[9]:


# Dropping unnecessary columns
df2 = df2.drop(['District'], axis= 1 )
df2


# In[10]:


# Changing the data type of numerical attributes
for i in range(4,10):
    df2.iloc[:,i] = pd.to_numeric(df2.iloc[:,i])


# In[12]:


df2[(df2['Area'] == 'INDIA') & (df2['Region'] == 'Total')]


# In[13]:


df3 = pd.DataFrame()


# In[14]:


# Creating a dataframe which contains total triligual speakers of each age group for every Area
for area in df2['Area'].unique():
    temp_df = df2[(df2['Area'].str.upper() == area.upper()) & (df2['Region'].str.upper() == 'TOTAL')].iloc[1:,:]
    temp_df.drop(['State','Region','Sec_Lang_Tot','Sec_Lang_M','Sec_Lang_F','Third_Lang_M','Third_Lang_F'], axis=1, inplace = True)
    df3 = pd.concat([df3, temp_df])
df3


# In[15]:


# Reading C-14 to find the age group wise population in each state
pop_df = pd.read_excel('DDW-0000C-14.xls')
pop_df.head(10)


# In[16]:


pop_df.columns = ['Table_Name','State_Code','District_Code','Area','Age_Group','Total_Person','Total_Male','Total_Female','Rural_Person',
                'Rural_Male','Rural_Female','Urban_Person','Urban_Male','Urban_Female']
pop_df.head(10)


# In[17]:


pop_df = pop_df.iloc[6:,:]
pop_df


# In[18]:


pop_df.reset_index(inplace=True,drop=True)
pop_df


# In[19]:


pop_df.columns


# In[20]:


# Dropping unnessecary columns
pop_df = pop_df.drop(['Table_Name', 'State_Code', 'District_Code','Total_Male', 'Total_Female', 'Rural_Person',
       'Rural_Male', 'Rural_Female', 'Urban_Person', 'Urban_Male',
       'Urban_Female'],axis=1)
pop_df


# In[21]:


# Adding population column
df3['Population'] = np.nan

df3


# In[22]:


df3.reset_index(drop=True,inplace=True)
df3


# In[23]:


pop_df


# In[24]:


pop_df[[True if 'ANDAMAN & NICOBAR ISLANDS' in i else False for i in pop_df['Area']]]


# In[25]:


pop_df2 = pop_df.copy()
pop_df2


# In[27]:


pop_df2['Total_Person'] = pd.to_numeric(pop_df2['Total_Person'])


# In[28]:


df3.head(20)


# In[29]:


pop_df2.head(20)


# #### As df3 has age groups which are merge of age groups present in pop_df2 (for example: df3 contains 30-49 while pop_df2 contains 30-34,35-39,40-44,45-49) so to find 30-49 population we have to sum the populations of 30-34,35-39,40-44,45-49 age groups in pop_df2

# In[30]:



i = 0
while i < pop_df.shape[0]:
    if '30' in pop_df2.loc[i,'Age_Group']:
        age_group_pop_sum = pop_df2.loc[i,'Total_Person']
        j = i + 1
        while not '49' in pop_df2.loc[j,'Age_Group']:
            age_group_pop_sum += pop_df2.loc[j,'Total_Person']
            pop_df2.drop(j,axis=0,inplace=True)
            j += 1
        age_group_pop_sum += pop_df2.loc[j,'Total_Person']
        pop_df2.drop(j,axis=0,inplace=True)
        pop_df2.loc[i,'Total_Person'] = age_group_pop_sum
        pop_df2.loc[i,'Age_Group'] = '30-49'
        i = j
        i += 1
        continue
        
    if '50' in pop_df2.loc[i,'Age_Group']:
        age_group_pop_sum = pop_df2.loc[i,'Total_Person']
        j = i + 1
        while not '69' in pop_df2.loc[j,'Age_Group']:
            age_group_pop_sum += pop_df2.loc[j,'Total_Person']
            pop_df2.drop(j,axis=0,inplace=True)
            j += 1
        age_group_pop_sum += pop_df2.loc[j,'Total_Person']
        pop_df2.drop(j,axis=0,inplace=True)
        pop_df2.loc[i,'Total_Person'] = age_group_pop_sum
        pop_df2.loc[i,'Age_Group'] = '50-69'
        i = j
        i += 1
        continue
        
    if '70' in pop_df2.loc[i,'Age_Group']:
        age_group_pop_sum = pop_df2.loc[i,'Total_Person']
        j = i + 1
        while not '80' in pop_df2.loc[j,'Age_Group']:
            age_group_pop_sum += pop_df2.loc[j,'Total_Person']
            pop_df2.drop(j,axis=0,inplace=True)
            j += 1
        age_group_pop_sum += pop_df2.loc[j,'Total_Person']
        pop_df2.drop(j,axis=0,inplace=True)
        pop_df2.loc[i,'Total_Person'] = age_group_pop_sum
        pop_df2.loc[i,'Age_Group'] = '70+'
        i = j
        i += 1
        continue
    
    i += 1


# In[31]:


pop_df2.head(20)


# In[32]:


pop_df2.reset_index(inplace=True,drop=True)
pop_df2


# In[33]:


# Finding the population of each age group from pop_df2 and adding it to df3
for i in df3.index:
    temp_df = pop_df2[[True if df3.iloc[i,0].upper() in area.upper() else False for area in pop_df2['Area']]]
    df3.iloc[i,3] = int(temp_df[temp_df['Age_Group'] == df3.iloc[i,1]].iloc[0]['Total_Person'])
df3


# In[34]:


df3.head(20)


# In[35]:


# Finding the percentage of people trilingual in each age group of every state
df3['Trilingual (%)'] = (df3['Third_Lang_Tot'] / df3['Population']) * 100
df3


# In[36]:


df4 = df3.drop(['Third_Lang_Tot','Population'],axis=1)
df4


# In[37]:


# Finding the age group for each state which has maximum percentage of trilingual people
idx = df4.groupby(['Area'])['Trilingual (%)'].transform(max) == df4['Trilingual (%)']
df5 = df4[idx]
df5


# In[38]:


df5.reset_index(drop=True, inplace=True)


# In[39]:


df5


# In[40]:


df5.columns = ['state/ut', 'age-group', 'percentage']
df5


# In[41]:


# Saving the results in age-india.csv inside Results directory
df5.to_csv('Results/age-india.csv',index=None)

