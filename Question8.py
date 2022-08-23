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


# Creating a dataframe which contains triligual, bilingual people of each age group for every Area
for area in df2['Area'].unique():
    temp_df = df2[(df2['Area'].str.upper() == area.upper()) & (df2['Region'].str.upper() == 'TOTAL')].iloc[1:,:]
    temp_df.drop(['State','Region','Sec_Lang_Tot','Third_Lang_Tot'], axis=1, inplace = True)
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
pop_df = pop_df.drop(['Table_Name', 'State_Code', 'District_Code','Total_Person', 'Rural_Person',
       'Rural_Male', 'Rural_Female', 'Urban_Person', 'Urban_Male',
       'Urban_Female'],axis=1)
pop_df


# In[21]:


df3


# In[22]:


# Adding population columns
df3['Male_Population'] = np.nan
df3['Female_Population'] = np.nan

df3


# In[23]:


df3.reset_index(drop=True,inplace=True)
df3


# In[24]:


pop_df


# In[25]:


pop_df[[True if 'ANDAMAN & NICOBAR ISLANDS' in i else False for i in pop_df['Area']]]


# In[26]:


pop_df2 = pop_df.copy()
pop_df2


# In[28]:


pop_df2['Total_Male'] = pd.to_numeric(pop_df2['Total_Male'])
pop_df2['Total_Female'] = pd.to_numeric(pop_df2['Total_Female'])


# In[29]:


df3.head(20)


# In[30]:


pop_df2.head(20)


# #### As df3 has age groups which are merge of age groups present in pop_df2 (for example: df3 contains 30-49 while pop_df2 contains 30-34,35-39,40-44,45-49) so to find 30-49 population we have to sum the populations of 30-34,35-39,40-44,45-49 age groups in pop_df2

# In[31]:



i = 0
while i < pop_df.shape[0]:
    if '30' in pop_df2.loc[i,'Age_Group']:
        age_group_male_sum = pop_df2.loc[i,'Total_Male']
        age_group_female_sum = pop_df2.loc[i,'Total_Female']
        j = i + 1
        while not '49' in pop_df2.loc[j,'Age_Group']:
            age_group_male_sum += pop_df2.loc[j,'Total_Male']
            age_group_female_sum += pop_df2.loc[j,'Total_Female']
            pop_df2.drop(j,axis=0,inplace=True)
            j += 1
        age_group_male_sum += pop_df2.loc[j,'Total_Male']
        age_group_female_sum += pop_df2.loc[j,'Total_Female']
        pop_df2.drop(j,axis=0,inplace=True)
        pop_df2.loc[i,'Total_Male'] = age_group_male_sum
        pop_df2.loc[i,'Total_Female'] = age_group_female_sum
        pop_df2.loc[i,'Age_Group'] = '30-49'
        i = j
        i += 1
        continue
        
    if '50' in pop_df2.loc[i,'Age_Group']:
        age_group_male_sum = pop_df2.loc[i,'Total_Male']
        age_group_female_sum = pop_df2.loc[i,'Total_Female']
        j = i + 1
        while not '69' in pop_df2.loc[j,'Age_Group']:
            age_group_male_sum += pop_df2.loc[j,'Total_Male']
            age_group_female_sum += pop_df2.loc[j,'Total_Female']
            pop_df2.drop(j,axis=0,inplace=True)
            j += 1
        age_group_male_sum += pop_df2.loc[j,'Total_Male']
        age_group_female_sum += pop_df2.loc[j,'Total_Female']
        pop_df2.drop(j,axis=0,inplace=True)
        pop_df2.loc[i,'Total_Male'] = age_group_male_sum
        pop_df2.loc[i,'Total_Female'] = age_group_female_sum
        pop_df2.loc[i,'Age_Group'] = '50-69'
        i = j
        i += 1
        continue
        
    if '70' in pop_df2.loc[i,'Age_Group']:
        age_group_male_sum = pop_df2.loc[i,'Total_Male']
        age_group_female_sum = pop_df2.loc[i,'Total_Female']
        j = i + 1
        while not '80' in pop_df2.loc[j,'Age_Group']:
            age_group_male_sum += pop_df2.loc[j,'Total_Male']
            age_group_female_sum += pop_df2.loc[j,'Total_Female']
            pop_df2.drop(j,axis=0,inplace=True)
            j += 1
        age_group_male_sum += pop_df2.loc[j,'Total_Male']
        age_group_female_sum += pop_df2.loc[j,'Total_Female']
        pop_df2.drop(j,axis=0,inplace=True)
        pop_df2.loc[i,'Total_Male'] = age_group_male_sum
        pop_df2.loc[i,'Total_Female'] = age_group_female_sum
        pop_df2.loc[i,'Age_Group'] = '70+'
        i = j
        i += 1
        continue
    
    i += 1


# In[32]:


pop_df2.head(20)


# In[33]:


pop_df2.reset_index(inplace=True,drop=True)
pop_df2


# In[34]:


df3


# In[35]:


# Finding the male/female population of each age group from pop_df2 and adding it to df3
for i in df3.index:
    temp_df = pop_df2[[True if df3.iloc[i,0].upper() in area.upper() else False for area in pop_df2['Area']]]
    df3.iloc[i,6] = int(temp_df[temp_df['Age_Group'] == df3.iloc[i,1]].iloc[0]['Total_Male'])
    df3.iloc[i,7] = int(temp_df[temp_df['Age_Group'] == df3.iloc[i,1]].iloc[0]['Total_Female'])
df3


# In[36]:


# Finding the people which speak exactly one and two languages 
df3['First_Lang_M'] = df3['Male_Population'] - df3['Sec_Lang_M']
df3['First_Lang_F'] = df3['Female_Population'] - df3['Sec_Lang_F']
df3['Sec_Lang_M'] = df3['Sec_Lang_M'] - df3['Third_Lang_M']
df3['Sec_Lang_F'] = df3['Sec_Lang_F'] - df3['Third_Lang_F']


# In[37]:


df3.head(20)


# ### Finding the age group for male,female that has maximum number of trilingual people in each state/ut

# In[38]:


ratio_of_3 = df3[['Area', 'Age_Group','Third_Lang_M',
       'Third_Lang_F', 'Male_Population', 'Female_Population']]
ratio_of_3


# In[39]:


# Calculating the percent trilingual people in each age group for both male, female
ratio_of_3['Trilingual_M (%)'] = (ratio_of_3['Third_Lang_M'] / ratio_of_3['Male_Population']) * 100
ratio_of_3['Trilingual_F (%)'] = (ratio_of_3['Third_Lang_F'] / ratio_of_3['Female_Population']) * 100
ratio_of_3


# In[40]:


# Keeping only trilingual male percentage column to find the age group with maximum percentage
ratio_of_3_M = ratio_of_3.drop(['Third_Lang_M', 'Third_Lang_F', 'Male_Population', 'Female_Population', 'Trilingual_F (%)'],axis=1)
ratio_of_3_M


# In[41]:


# Keeping only trilingual female percentage column to find the age group with maximum percentage

ratio_of_3_F = ratio_of_3.drop(['Third_Lang_M', 'Third_Lang_F', 'Male_Population', 'Female_Population', 'Trilingual_M (%)'],axis=1)
ratio_of_3_F


# In[42]:


# Finding the age group for each state which has maximum percentage of trilingual males
idx = ratio_of_3_M.groupby(['Area'])['Trilingual_M (%)'].transform(max) == ratio_of_3_M['Trilingual_M (%)']
result_ratio_of_3_M = ratio_of_3_M[idx]
result_ratio_of_3_M


# In[43]:


# Finding the age group for each state which has maximum percentage of trilingual females
idx = ratio_of_3_F.groupby(['Area'])['Trilingual_F (%)'].transform(max) == ratio_of_3_F['Trilingual_F (%)']
result_ratio_of_3_F = ratio_of_3_F[idx]
result_ratio_of_3_F


# In[44]:


result_ratio_of_3_M.reset_index(drop=True,inplace=True)
result_ratio_of_3_F.reset_index(drop=True,inplace=True)


# In[45]:


# Concatanating both results
result_ratio_of_3 = result_ratio_of_3_M.copy()
result_ratio_of_3['age_Group_female'] = result_ratio_of_3_F['Age_Group']
result_ratio_of_3['ratio-of-3-female'] = result_ratio_of_3_F['Trilingual_F (%)']
result_ratio_of_3.columns = ['state/ut','age-group-males','ratio-males','age-group-females','ratio-females']
result_ratio_of_3


# In[46]:


# Storing the result in age-gender-a, It contains female and male age groups with maximum percent of trilingual people
# in whole state/ut
result_ratio_of_3.to_csv('Results/age-gender-a.csv',index=False)


# ### Finding the age group for male,female that has maximum number of bilingual people in each state/ut

# In[47]:


ratio_of_2 = df3[['Area', 'Age_Group','Sec_Lang_M',
       'Sec_Lang_F', 'Male_Population', 'Female_Population']]
ratio_of_2


# In[48]:


# Calculating the percent bilingual people in each age group for both male, female
ratio_of_2['Bilingual_M (%)'] = (ratio_of_2['Sec_Lang_M'] / ratio_of_2['Male_Population']) * 100
ratio_of_2['Bilingual_F (%)'] = (ratio_of_2['Sec_Lang_F'] / ratio_of_2['Female_Population']) * 100
ratio_of_2


# In[49]:


# Keeping only bilingual male percentage column to find the age group with maximum percentage
ratio_of_2_M = ratio_of_2.drop(['Sec_Lang_M', 'Sec_Lang_F', 'Male_Population', 'Female_Population', 'Bilingual_F (%)'],axis=1)
ratio_of_2_M


# In[50]:


# Keeping only bilingual female percentage column to find the age group with maximum percentage
ratio_of_2_F = ratio_of_2.drop(['Sec_Lang_M', 'Sec_Lang_F', 'Male_Population', 'Female_Population', 'Bilingual_M (%)'],axis=1)
ratio_of_2_F


# In[51]:


# Finding the age group for each state which has maximum percentage of bilingual males

idx = ratio_of_2_M.groupby(['Area'])['Bilingual_M (%)'].transform(max) == ratio_of_2_M['Bilingual_M (%)']
result_ratio_of_2_M = ratio_of_2_M[idx]
result_ratio_of_2_M


# In[52]:


# Finding the age group for each state which has maximum percentage of bilingual females
idx = ratio_of_2_F.groupby(['Area'])['Bilingual_F (%)'].transform(max) == ratio_of_2_F['Bilingual_F (%)']
result_ratio_of_2_F = ratio_of_2_F[idx]
result_ratio_of_2_F


# In[53]:


result_ratio_of_2_M.reset_index(drop=True,inplace=True)
result_ratio_of_2_F.reset_index(drop=True,inplace=True)


# In[54]:


# Concatanating both results
result_ratio_of_2 = result_ratio_of_2_M.copy()
result_ratio_of_2['age_Group_female'] = result_ratio_of_2_F['Age_Group']
result_ratio_of_2['ratio-of-2-female'] = result_ratio_of_2_F['Bilingual_F (%)']
result_ratio_of_2.columns = ['state/ut','age-group-males','ratio-males','age-group-females','ratio-females']
result_ratio_of_2


# In[55]:


# Storing the result in age-gender-b, It contains female and male age groups with maximum percent 
# of bilingual people in whole state/ut
result_ratio_of_2.to_csv('Results/age-gender-b.csv',index=None)


# ### Finding the age group for male,female that has maximum number of Monolingual people in each state/ut

# In[56]:


ratio_of_1 = df3[['Area', 'Age_Group','First_Lang_M',
       'First_Lang_F', 'Male_Population', 'Female_Population']]
ratio_of_1


# In[57]:


# Calculating the percent Monolingual people in each age group for both male, female
ratio_of_1['Monolingual_M (%)'] = (ratio_of_1['First_Lang_M'] / ratio_of_1['Male_Population']) * 100
ratio_of_1['Monolingual_F (%)'] = (ratio_of_1['First_Lang_F'] / ratio_of_1['Female_Population']) * 100
ratio_of_1


# In[58]:


# Keeping only Monolingual male percentage column to find the age group with maximum percentage

ratio_of_1_M = ratio_of_1.drop(['First_Lang_M', 'First_Lang_F', 'Male_Population', 'Female_Population', 'Monolingual_F (%)'],axis=1)
ratio_of_1_M


# In[59]:


# Keeping only monolingual female percentage column to find the age group with maximum percentage
ratio_of_1_F = ratio_of_1.drop(['First_Lang_M', 'First_Lang_F', 'Male_Population', 'Female_Population', 'Monolingual_M (%)'],axis=1)
ratio_of_1_F


# In[60]:


# Finding the age group for each state which has maximum percentage of monolingual males
idx = ratio_of_1_M.groupby(['Area'])['Monolingual_M (%)'].transform(max) == ratio_of_1_M['Monolingual_M (%)']
result_ratio_of_1_M = ratio_of_1_M[idx]
result_ratio_of_1_M


# In[61]:


# Finding the age group for each state which has maximum percentage of monolingual females
idx = ratio_of_1_F.groupby(['Area'])['Monolingual_F (%)'].transform(max) == ratio_of_1_F['Monolingual_F (%)']
result_ratio_of_1_F = ratio_of_1_F[idx]
result_ratio_of_1_F


# In[62]:


result_ratio_of_1_M.reset_index(drop=True,inplace=True)
result_ratio_of_1_F.reset_index(drop=True,inplace=True)


# In[63]:


# Concatanating both results
result_ratio_of_1 = result_ratio_of_1_M.copy()
result_ratio_of_1['age_Group_female'] = result_ratio_of_1_F['Age_Group']
result_ratio_of_1['ratio-of-1-female'] = result_ratio_of_1_F['Monolingual_F (%)']
result_ratio_of_1


# In[64]:


# Storing the result in age-gender-c, It contains female and male age groups with maximum percent 
# of monolingual people in whole state/ut
result_ratio_of_1.columns = ['state/ut','age-group-males','ratio-males','age-group-females','ratio-females']

result_ratio_of_1.to_csv('Results/age-gender-c.csv',index=None)

