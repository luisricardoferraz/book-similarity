#!/usr/bin/env python
# coding: utf-8

# In[29]:


#Import packages
import pandas as pd
from pandas import DataFrame


# In[42]:


#Define where's the CSV file
filePath = 'C:/Users/LuisRicardoFerraz/Documents/personal/projects/book-similarity/test/tutorial/tutorial/spiders/bookListSpider.csv'


# In[112]:


#Import CSV file to a DataFrame
df = pd.read_csv(filePath)


# In[114]:


#Remove duplicates from DataFrame
df = df.drop_duplicates(subset=['isbn-10','isbn-13','titulo'],keep='first',inplace=False)


# In[115]:


#Remove null fields from a list of columns in DataFrame
df = df.dropna(axis=0,how='any',subset=['isbn-10','isbn-13','titulo','autor','editora','ano','paginas','idioma','leram','lendo','queremLer','relendo','abandonos','resenhas','rating','favoritos','desejados','trocam','avaliaram','cincoEstrelas','quatroEstrelas','tresEstrelas','duasEstrelas','umaEstrela','avaliacoesHomens','avaliacoesMulheres','generos','sinopse'],inplace=False)


# In[116]:


#Export DataFrame to a new CSV file
df.to_csv('C:/Users/LuisRicardoFerraz/Documents/personal/projects/book-similarity/test/tutorial/tutorial/spiders/novo_dataframe.csv')

