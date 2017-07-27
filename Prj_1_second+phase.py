
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import timeit
    
nyc_data=pd.read_excel("D:/Jalsha deck/Copy of Keywords_extended_list.xlsx")
nyc_data

    # extracted the topics 

col_names=[i for i in nyc_data.columns]
topics=[]
for i in range(0,len(col_names),5):
    topics.append(col_names[i])

    # extract the extended list 1 and status 1 for all values where the status is yes 

import fnmatch
pattern = '*_*'
col_names_filtered_status_extended= fnmatch.filter(col_names, pattern)
print(len(col_names_filtered_status_extended))
print(len(topics))

    # create a list having only columns that are required

new_columns=[]
c=0
for i in range(0,len(topics)):
    c=i*2
    # multiple append using extend
    new_columns.extend((topics[i],col_names_filtered_status_extended[c],col_names_filtered_status_extended[c+1]))
print(len(new_columns))
print(new_columns)

    # create a df's
for i in range(0,len(new_columns)//3):
    c=i*3
    new_df=nyc_data[new_columns[c:c+3]]
    t=new_df[new_df.iloc[:,2]=='Yes']

# Code to create a dictionary bsed on topics
topic_dict=[]
for i in range(0,len(new_columns)//3):
    c=i*3
    new_df=nyc_data[new_columns[c:c+3]]
    t=new_df[new_df.ix[:,2]=='Yes']
    x=[t.columns]
    x1=x[0][2]
    t.drop(x1,axis=1,inplace=True)
    x2=x[0][0]
    x3=x[0][1]
    # create a length series for extracting the length of 1st column
    t.iloc[:,0]=np.where(t.iloc[:,1]=='</s>',t.iloc[:,0],t.iloc[:,1])
    new=t.iloc[:,0]
    # convert to dictionary after cleaning
    key=[i.replace('_'," ") for i in new]
    key=[i.replace('</s>'," ") for i in key]
    key=[i.replace('( 1 )'," ") for i in key]
    key=[i.replace('( 0 )'," ") for i in key]
    key=[i.replace('( 2 )'," ") for i in key]
    key=[i.replace('( 171 )'," ") for i in key]
    key=[i.replace('( 3 )'," ") for i in key]
    key=[i.replace('( 22 )'," ") for i in key]
    key=[i.strip() for i in key]
    val=[t.columns[0] for i in range(0,len(key))]
    topic_dict.append(dict( zip( key, val)))

topic_dict


# In[32]:

# each dict values 
# unique values for each list
#x=[for i in range(0,len(topic_dict))]
#for i in range(0,len(topic_dict)):
    #print(len(topic_dict[i].values()))
all_keywords=[]
for i in range(0,len(topic_dict)):
    all_keywords.append(topic_dict[i].keys())
    


# In[33]:

# check duplicates - test the kewys of 1 dict with others


# In[2]:

type(topic_dict)
df=pd.read_csv('D:/Jalsha deck/WEB_SCRAPED_DATA_BSB.csv')
scripts=df['Summary_telly']

def check_present(x):
    if any(topic.keys() in x for topic in topic_dict):
        return (1)
#check_present[scripts.iloc[0]]
for i in scripts:
        


# In[ ]:




# In[4]:

each_line=[]
for i in scripts:
    each_line.append(i)
    for j in range(0,len(topic_dict)):
        if any(topic_dict[j].keys() in i for k in i):
            print(1)
        else:
            print(0)


# In[5]:

each_line=[]
for i in scripts:
    each_line.append(i)
    print(each_line)
    each_line.pop
each_line


# In[ ]:



