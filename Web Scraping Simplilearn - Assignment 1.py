#!/usr/bin/env python
# coding: utf-8

# 
# # **Web scraping**

# 
# Web scraping, also known as web harvesting or web data extraction, is a type of data scraping used to gather information from websites.

# In this session, we will cover the following concepts with the help of a business use case:
#   * Data acquisition through Web scraping

# - Warnings are given to developers to alert them about circumstances that are not necessarily exceptions. Warnings are not the same as errors. It shows some message but the program will run. The `filterwarnings()` function, defined in the `warning` module, is used to handle warnings (presented, disregarded, or raised to exceptions).

# In[1]:


import warnings
warnings.filterwarnings("ignore")


# #### Health Care Rankings for Different European Countries

#     * Beautiful Soup is a Python package that is used for web scraping. The urllib package is used to simplify the tasks of building, loading and parsing URLs. The Python datetime module supplies classes to work with date and time.

# In[2]:


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import re
import urllib.request as urllib2
from datetime import datetime
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


#     * We are going to scrape data from Wikipedia. The data indicate rankings on different health indices such as patient rights and information, accessibility (waiting time for treatment), outcomes, range, the reach of services provided, prevention, and pharmaceuticals. The data are from the Euro Health Consumer index. In the following code, we read the data and use Beautiful Soup to convert the data into **bs4.BeautifulSoup** data.

# In[35]:


url = 'https://en.wikipedia.org/wiki/Healthcare_in_Europe' 
r = requests.get(url)
HCE = BeautifulSoup(r.text)
type(HCE)


# - First, we must choose the table that we want to scrape. As many webpages have tables, we'll retrieve the exact table names from the HTML and store them in a list called `lst.`

# In[36]:


webpage = urllib2.urlopen(url)
htmlpage= webpage.readlines()
lst = []
for line in htmlpage:
    line = str(line).rstrip()
    if re.search('table class', line) :
        lst.append(line)


# In[37]:


len(lst)


# - This list `lst` has a length of 5.

# - Now let us display `lst`.

# In[32]:


lst


# - We will scrape the first table, and use index 0 in `lst` to capture the first table name. Now, read the table using Beautiful Soup's `find` function. A simple option is to type the table name. You can simply select the name in `lst`, which in this case is "wikitable floatright sortable".

# In[33]:


table=HCE.find('table', {'class', 'wikitable floatright sortable'})


# In[39]:


table


# - Alternatively, there is a way to automate this step by capturing the first data from the list and then stripping off the unnecessary characters like `^ " *`.

# In[40]:


type(table)


# In[9]:


x=lst[0]
extr=re.findall('"([^"]*)"', x)
table=HCE.find('table', {'class', extr[0]})


# In[10]:


type(table)


# - Now, it would be good to read the header and row names separately, so later we can easily make a DataFrame.

# In[43]:


headers= [header.text for header in table.find_all('th')]


# In[44]:


headers


# In[45]:


# Remove '\n' , '\t', '\p' & other noisy tags . String method strip() to elliminate unwanted characters.
headers[:] = [headers.strip('\n') for headers in headers]


# In[46]:


headers


# In[47]:


rows = []
for row in table.find_all('tr'):
    rows.append([val.text.encode('utf8').decode() for val in row.find_all('td')])


# - Now, all elements, rows, and headers are available to build the DataFrame, which we will call `df1`.

# In[48]:


df1 = pd.DataFrame(rows, columns=headers)


# - Let's display first seven rows of the `df1`

# In[15]:


df1.head(7)


# In[49]:


def preproc(dat):
    dat.dropna(axis=0, how='all', inplace=True)
    dat.columns = dat.columns.str.replace("\n", "")
    dat.replace(["\n"], [""], regex=True, inplace=True)
    dat.replace([r"\s\*$"], [""], regex=True, inplace=True)
    dat.replace([","], [""], regex=True, inplace=True)
    dat.replace(r"\b[a-zA-Z]\b", np.nan, regex=True, inplace=True)
    dat.replace([r"^\s"], [""], regex=True, inplace=True)
    dat = dat.apply(pd.to_numeric, errors='ignore')    
    return(dat)


# In[50]:


df1 = preproc(df1)


# In[51]:


df1


# #### Health Expenditure

# Let's scrape health expenditure as well. These are data per capita, which means that expenditure was corrected for the number of habitants in a country.
# 
# - Just like we did for above web page (**Health Care Rankings for Different European Countries**), we have to repeat the same steps in this web page as well (**Health Expenditure**).
# 
# - Finally, we will be directed to the first table "wikitable sortable static" in this web page as well.

# In[16]:


url = 'https://en.wikipedia.org/wiki/List_of_countries_by_total_health_expenditure_per_capita' 
r = requests.get(url)
HEE = BeautifulSoup(r.text)
webpage = urllib2.urlopen(url)
htmlpage= webpage.readlines()
lst = []
for line in htmlpage:
    line = str(line).rstrip()
    if re.search('table class', line) :
        lst.append(line)
x=lst[1]
print(x)
extr=re.findall('"([^"]*)"', x)
table=HEE.find('table', {'class', extr[0]})
headers= [header.text for header in table.find_all('th')]
rows = []
for row in table.find_all('tr'):
    rows.append([val.text.encode('utf8').decode() for val in row.find_all('td')])
headers = [i.replace("\n", "") for i in headers]
df2 = pd.DataFrame(rows, columns=headers)


# - Let's display the first five rows of the table "wikitable sortable static"

# In[17]:


df2.head()


# #### Additional Preprocessing Steps
# If we look at the DataFrame, we can see that there are still some issues that prohibit numeric computations. 

#     * There are undesired characters ('\n') 
#     * The undesired decimal format (,) should be removed
#     * There are cells with non-numeric characters ('x') that should be NAN

# In[18]:


def preproc(dat):
    dat.dropna(axis=0, how='all', inplace=True)
    dat.columns = dat.columns.str.replace("\n", "")
    dat.replace(["\n"], [""], regex=True, inplace=True)
    dat.replace([r"\s\*$"], [""], regex=True, inplace=True)
    dat.replace([","], [""], regex=True, inplace=True)
    dat.replace(r"\b[a-zA-Z]\b", np.nan, regex=True, inplace=True)
    dat.replace([r"^\s"], [""], regex=True, inplace=True)
    dat = dat.apply(pd.to_numeric, errors='ignore')    
    return(dat)


# In[19]:


df1 = preproc(df1)
df2 = preproc(df2)


#     * Apparently, after this preprocessing, there are some NANs.

# In[20]:


print(df1.isnull().sum().sum())
print(df2.isnull().sum().sum())


#     * Now we display where the NANs occur. In fact, when we check the original table, we can see that Cyprus has values "x", which were in our preproc function changed to NANs ( https://en.wikipedia.org/wiki/Healthcare_in_Europe ).

# In[21]:


df1[df1.isnull().any(axis=1)]


# #### Handling Missing Values
#     * Remove NA values

# In[22]:


df1.dropna(axis=0, how='any', inplace=True)


# At this point we inspect the data types:

# In[23]:


df1.dtypes


# In[24]:


df2.dtypes


# The column names are a bit long, so it would be good to use shorter names.

# In[25]:


df1.columns = ['WorldRank', 'EURank', 'Country', 'Life expectancy in (years)']
df2.columns = ['Country', '2017', '2018', '2019']


# #### Analyzing Final Tables 

# In[26]:


df1.head()


# In[27]:


df2.head()


# 
# ## **Merging Different Data**

# It should be clear from this example that web scraping can be important to quickly grasp data.
# Web scraping may be particularly useful when you need to automate data processing:
#  
#     * Webdata change regularly and need to be stored repeatedly.
#  
#     * A large number of data sources, for example, tables, need to be loaded and merged.
#  
# Let us elaborate on the last point a bit more. If the two tables that we just scraped need to be merged, it can be done in Python. For example, if we want to merge on the column "Country", we would use the following code (we use the `.head()` function to limit the output).
# 

# In[28]:


pd.merge(df1, df2, how='left', on='Country').head()


# **Note: In this lesson, we saw the use of the data wrangling and web scraping methods, but in the next lesson we are going to use one of these methods as a sub component of "Feature Engineering".**
