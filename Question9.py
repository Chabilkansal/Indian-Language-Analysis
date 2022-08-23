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
    temp_df.drop(['State','Region','Sec_Lang_Tot','Third_Lang_Tot'], axis=1, inplace = True)
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


# In[21]:


pop_df.columns


# In[22]:


# As in C-19 csv (df3) some literacy levels are merged with other literacy levels so merge there literacy levels in pop_df too 
pop_df['Literate_M'] = pop_df['Literate_M'] + pop_df['Literate_w/o_education_level_M'] + pop_df['Unclassified_M']
pop_df['Literate_F'] = pop_df['Literate_F'] + pop_df['Literate_w/o_education_level_F'] + pop_df['Unclassified_F']
pop_df['Matric_M'] = pop_df['Matric_M'] + pop_df['NonTechnical_Diploma_M'] + pop_df['Technical_Diploma_M'] + pop_df['Intermediate_M']
pop_df['Matric_F'] = pop_df['Matric_F'] + pop_df['NonTechnical_Diploma_F'] + pop_df['Technical_Diploma_F'] + pop_df['Intermediate_F']


# In[23]:


pop_df


# In[24]:


pop_df.columns


# In[25]:


# Dropping unnessecary columns
pop_df = pop_df.drop(['Table_Name', 'State_Code', 'District_Code','Total_P','Total_M', 'Total_F','Illiterate_P',
                      'Literate_P','Literate_w/o_education_level_P',
                      'Literate_w/o_education_level_M','Literate_w/o_education_level_F','Below_Primary_P',
                     'Primary_P','Middle_P','Matric_P',
                     'Intermediate_P','Intermediate_M','Intermediate_F','NonTechnical_Diploma_P',
                      'NonTechnical_Diploma_M','NonTechnical_Diploma_F', 'Technical_Diploma_P',
                      'Technical_Diploma_M','Technical_Diploma_F','Graduate_P',
                     'Unclassified_P', 'Unclassified_M', 'Unclassified_F'],axis=1)
pop_df


# In[26]:


# Adding population column
df3['Male_Population'] = np.nan
df3['Female_Population'] = np.nan
df3


# In[27]:


df3.reset_index(drop=True, inplace=True)
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
        df3.iloc[i,6] = int(temp_df.iloc[0]['Illiterate_M'])
        df3.iloc[i,7] = int(temp_df.iloc[0]['Illiterate_F'])
    elif df3.iloc[i,1] == 'Literate':    
        df3.iloc[i,6] = int(temp_df.iloc[0]['Literate_M'])
        df3.iloc[i,7] = int(temp_df.iloc[0]['Literate_F'])
    elif df3.iloc[i,1] == 'Literate but below primary':    
        df3.iloc[i,6] = int(temp_df.iloc[0]['Below_Primary_M'])
        df3.iloc[i,7] = int(temp_df.iloc[0]['Below_Primary_F'])
    elif df3.iloc[i,1] == 'Primary but below middle':    
        df3.iloc[i,6] = int(temp_df.iloc[0]['Primary_M'])
        df3.iloc[i,7] = int(temp_df.iloc[0]['Primary_F'])
    elif df3.iloc[i,1] == 'Middle but below matric/secondary':    
        df3.iloc[i,6] = int(temp_df.iloc[0]['Middle_M'])
        df3.iloc[i,7] = int(temp_df.iloc[0]['Middle_F'])
    elif df3.iloc[i,1] == 'Matric/Secondary but below graduate':    
        df3.iloc[i,6] = int(temp_df.iloc[0]['Matric_M'])
        df3.iloc[i,7] = int(temp_df.iloc[0]['Matric_F'])
    elif df3.iloc[i,1] == 'Graduate and above':    
        df3.iloc[i,6] = int(temp_df.iloc[0]['Graduate_M'])
        df3.iloc[i,7] = int(temp_df.iloc[0]['Graduate_F'])
df3


# In[32]:


df3.head(20)


# In[33]:


df3['First_Lang_M'] = df3['Male_Population'] - df3['Sec_Lang_M']
df3['First_Lang_F'] = df3['Female_Population'] - df3['Sec_Lang_F']
df3['Sec_Lang_M'] = df3['Sec_Lang_M'] - df3['Third_Lang_M']
df3['Sec_Lang_F'] = df3['Sec_Lang_F'] - df3['Third_Lang_F']


# In[34]:


df3


# ### Finding the Literacy level for male,female that has maximum number of trilingual people in each state/ut

# In[35]:


ratio_of_3 = df3[['Area', 'Education_Level','Third_Lang_M',
       'Third_Lang_F', 'Male_Population', 'Female_Population']]
ratio_of_3


# In[36]:


# Calculating the percent trilingual people at each literacy level for both male, female
ratio_of_3['Trilingual_M (%)'] = (ratio_of_3['Third_Lang_M'] / ratio_of_3['Male_Population']) * 100
ratio_of_3['Trilingual_F (%)'] = (ratio_of_3['Third_Lang_F'] / ratio_of_3['Female_Population']) * 100
ratio_of_3


# In[37]:


# Keeping only trilingual male percentage column to find the literacy level with maximum percentage
ratio_of_3_M = ratio_of_3.drop(['Third_Lang_M', 'Third_Lang_F', 'Male_Population', 'Female_Population', 'Trilingual_F (%)'],axis=1)
ratio_of_3_M


# In[38]:


# Keeping only trilingual female percentage column to find the literacy level with maximum percentage

ratio_of_3_F = ratio_of_3.drop(['Third_Lang_M', 'Third_Lang_F', 'Male_Population', 'Female_Population', 'Trilingual_M (%)'],axis=1)
ratio_of_3_F


# In[39]:


# Finding the literacy level for each state which has maximum percentage of trilingual males
idx = ratio_of_3_M.groupby(['Area'])['Trilingual_M (%)'].transform(max) == ratio_of_3_M['Trilingual_M (%)']
result_ratio_of_3_M = ratio_of_3_M[idx]
result_ratio_of_3_M


# In[40]:


# Finding the literacy level for each state which has maximum percentage of trilingual females
idx = ratio_of_3_F.groupby(['Area'])['Trilingual_F (%)'].transform(max) == ratio_of_3_F['Trilingual_F (%)']
result_ratio_of_3_F = ratio_of_3_F[idx]
result_ratio_of_3_F


# In[41]:


result_ratio_of_3_M.reset_index(drop=True,inplace=True)
result_ratio_of_3_F.reset_index(drop=True,inplace=True)


# In[42]:


# Concatanating both results
result_ratio_of_3 = result_ratio_of_3_M.copy()
result_ratio_of_3['Edu_Level_female'] = result_ratio_of_3_F['Education_Level']
result_ratio_of_3['ratio-of-3-female'] = result_ratio_of_3_F['Trilingual_F (%)']
result_ratio_of_3.columns = ['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females']
result_ratio_of_3


# In[43]:


# Storing the result in literacy-gender-a, It contains female and male literacy level with maximum percent of trilingual people
# in whole state/ut
result_ratio_of_3.to_csv('Results/literacy-gender-a.csv',index=False)


# ### Finding the literacy level for male,female that has maximum number of bilingual people in each state/ut

# In[44]:


ratio_of_2 = df3[['Area', 'Education_Level','Sec_Lang_M',
       'Sec_Lang_F', 'Male_Population', 'Female_Population']]
ratio_of_2


# In[45]:


# Calculating the percent bilingual people at each literacy level for both male, female
ratio_of_2['Bilingual_M (%)'] = (ratio_of_2['Sec_Lang_M'] / ratio_of_2['Male_Population']) * 100
ratio_of_2['Bilingual_F (%)'] = (ratio_of_2['Sec_Lang_F'] / ratio_of_2['Female_Population']) * 100
ratio_of_2


# In[46]:


# Keeping only bilingual male percentage column to find the literacy level with maximum percentage
ratio_of_2_M = ratio_of_2.drop(['Sec_Lang_M', 'Sec_Lang_F', 'Male_Population', 'Female_Population', 'Bilingual_F (%)'],axis=1)
ratio_of_2_M


# In[47]:


# Keeping only bilingual female percentage column to find the literacy level with maximum percentage
ratio_of_2_F = ratio_of_2.drop(['Sec_Lang_M', 'Sec_Lang_F', 'Male_Population', 'Female_Population', 'Bilingual_M (%)'],axis=1)
ratio_of_2_F


# In[48]:


# Finding the literacy level for each state which has maximum percentage of bilingual males

idx = ratio_of_2_M.groupby(['Area'])['Bilingual_M (%)'].transform(max) == ratio_of_2_M['Bilingual_M (%)']
result_ratio_of_2_M = ratio_of_2_M[idx]
result_ratio_of_2_M


# In[49]:


# Finding the literacy level for each state which has maximum percentage of bilingual females
idx = ratio_of_2_F.groupby(['Area'])['Bilingual_F (%)'].transform(max) == ratio_of_2_F['Bilingual_F (%)']
result_ratio_of_2_F = ratio_of_2_F[idx]
result_ratio_of_2_F


# In[50]:


result_ratio_of_2_M.reset_index(drop=True,inplace=True)
result_ratio_of_2_F.reset_index(drop=True,inplace=True)


# In[51]:


# Concatanating both results
result_ratio_of_2 = result_ratio_of_2_M.copy()
result_ratio_of_2['edu-level-female'] = result_ratio_of_2_F['Education_Level']
result_ratio_of_2['ratio-of-2-female'] = result_ratio_of_2_F['Bilingual_F (%)']
result_ratio_of_2.columns = ['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females']
result_ratio_of_2


# In[52]:


# Storing the result in literacy-gender-b, It contains female and male literacy levels with maximum percent 
# of bilingual people in whole state/ut
result_ratio_of_2.to_csv('Results/literacy-gender-b.csv',index=None)


# ### Finding the literacy level for male,female that has maximum number of Monolingual people in each state/ut

# In[53]:


ratio_of_1 = df3[['Area', 'Education_Level','First_Lang_M',
       'First_Lang_F', 'Male_Population', 'Female_Population']]
ratio_of_1


# In[54]:


# Calculating the percent Monolingual people at each literacy level for both male, female
ratio_of_1['Monolingual_M (%)'] = (ratio_of_1['First_Lang_M'] / ratio_of_1['Male_Population']) * 100
ratio_of_1['Monolingual_F (%)'] = (ratio_of_1['First_Lang_F'] / ratio_of_1['Female_Population']) * 100
ratio_of_1


# In[55]:


# Keeping only Monolingual male percentage column to find the literacy level with maximum percentage

ratio_of_1_M = ratio_of_1.drop(['First_Lang_M', 'First_Lang_F', 'Male_Population', 'Female_Population', 'Monolingual_F (%)'],axis=1)
ratio_of_1_M


# In[56]:


# Keeping only monolingual female percentage column to find the literacy level with maximum percentage
ratio_of_1_F = ratio_of_1.drop(['First_Lang_M', 'First_Lang_F', 'Male_Population', 'Female_Population', 'Monolingual_M (%)'],axis=1)
ratio_of_1_F


# In[57]:


# Finding the literacy level for each state which has maximum percentage of monolingual males
idx = ratio_of_1_M.groupby(['Area'])['Monolingual_M (%)'].transform(max) == ratio_of_1_M['Monolingual_M (%)']
result_ratio_of_1_M = ratio_of_1_M[idx]
result_ratio_of_1_M


# In[58]:


# Finding the literacy level for each state which has maximum percentage of monolingual females
idx = ratio_of_1_F.groupby(['Area'])['Monolingual_F (%)'].transform(max) == ratio_of_1_F['Monolingual_F (%)']
result_ratio_of_1_F = ratio_of_1_F[idx]
result_ratio_of_1_F


# In[59]:


result_ratio_of_1_M.reset_index(drop=True,inplace=True)
result_ratio_of_1_F.reset_index(drop=True,inplace=True)


# In[60]:


# Concatanating both results
result_ratio_of_1 = result_ratio_of_1_M.copy()
result_ratio_of_1['edu-level-female'] = result_ratio_of_1_F['Education_Level']
result_ratio_of_1['ratio-of-1-female'] = result_ratio_of_1_F['Monolingual_F (%)']
result_ratio_of_1


# In[61]:


# Storing the result in literacy-gender-c, It contains female and male literacy levels with maximum percent 
# of monolingual people in whole state/ut
result_ratio_of_1.columns = ['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females']

result_ratio_of_1.to_csv('Results/literacy-gender-c.csv',index=None)


# In[ ]:




