#!/usr/bin/env python
# coding: utf-8

# In[65]:


#Import packages
import pandas as pd
from pandas import DataFrame
import re


# In[2]:


#Define where's the CSV file
filePath = 'C:/Users/LuisRicardoFerraz/Documents/personal/projects/book-similarity/test/tutorial/tutorial/spiders/newDataSet.csv'


# In[3]:


#Import CSV file to a DataFrame
df = pd.read_csv(filePath)


# In[7]:


#Remove null fields from a list of columns in DataFrame
df = df.dropna(axis=0,how='any',subset=['isbn-10','isbn-13','titulo','autor','editora','ano','paginas','leram','lendo','queremLer','relendo','abandonos','resenhas','nota','favoritos','desejados','trocam','avaliaram','cincoEstrelas','quatroEstrelas','tresEstrelas','duasEstrelas','umaEstrela','avaliacoesHomens','avaliacoesMulheres','sinopse'],inplace=False)


# In[9]:


for string in df.columns:
    df[string] = [str(item).strip() for item in df[string]]


# In[12]:


#Remove duplicates from DataFrame
df = df.drop_duplicates(subset=['isbn-10','isbn-13','titulo'],keep='first',inplace=False)


# In[15]:


df = df[df['ano'].map(len) == 9]
df['ano'] = [ano.replace('Ano: ', '') for ano in df['ano']]


# In[17]:


df = df[df['idioma'].map(len) == 17]
df['idioma'] = [idioma.replace('Idioma: ', '') for idioma in df['idioma']]


# In[21]:


df['paginas'] = [pagina.replace('Páginas: ', '') for pagina in df['paginas']]


# In[38]:


for column in ['favoritos','desejados','trocam','avaliaram']:
    df[column] = [re.search('[0-9]+',value).group() for value in df[column]]


# In[60]:


def removePercentage(value):
    return int(value.replace('%',''))/100


# In[63]:


for column in ['cincoEstrelas','quatroEstrelas','tresEstrelas','duasEstrelas','umaEstrela','avaliacoesHomens','avaliacoesMulheres']:
    df[column] = [removePercentage(value) for value in df[column]]


# In[64]:


#Export DataFrame to a new CSV file
df.to_csv('C:/Users/LuisRicardoFerraz/Documents/personal/projects/book-similarity/test/tutorial/tutorial/spiders/newDatasetClean.csv')

