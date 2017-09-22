import pandas as pd
import re
from nltk import sent_tokenize
from nltk import word_tokenize
import os
import glob
import numpy as np

# MASTER  DATA FRAME IS THE SYNOPSIS DATA 

def REMOVE_SPECIAL_CHARS(text):
    text=str(text).replace('^^','')
    text.replace('episode','').replace('online','')
    text=re.sub('[^a-zA-Z]+', ' ', text)
    return text


def TOPIC_DF(data_frame_name_with_csv):
    topic_df=pd.read_csv(data_frame_name_with_csv)
    return topic_df


def FILTER_MASTER_DATA_WITH_DATE(data_frame_name,master_data_frame_name):
    year=data_frame_name[6:10]
    month=data_frame_name.replace('.csv','')[11:len(data_frame_name)]
    filtered_df=master_data_frame_name[((master_data_frame_name.TXDate.dt.month)==np.int64(month)) & 
                                       (master_data_frame_name.TXDate.dt.year==np.int64(year)) ]
    master_df=filtered_df.reset_index()
    master_df=master_df[['Synopsis','Noun','TXDate']]
    return master_df


def GET_ALL_TOPIC_NAMES_FROM_TOPIC(topic_data_frame_name):
    
    topic1=list(str(topic_data_frame_name['Topic 1']))
    topic1=map(list, topic_data_frame_name['Topic 1'])
    topic2=list(str(topic_data_frame_name['Topic 2']))
    topic2=map(list, topic_data_frame_name['Topic 2'])
    topic3=list(str(topic_data_frame_name['Topic 2']))
    topic3=map(list, topic_data_frame_name['Topic 3'])
    topic1=[''.join(i) for i in topic1]
    topic2=[''.join(i) for i in topic2]
    topic3=[''.join(i) for i in topic3]
    all_topic=topic1+topic2+topic3
    return all_topic


def TOPIC_TAGGING_FUNCTION(text):
        
        sentences = sent_tokenize(text)
        tokenized_sentences = [word_tokenize(word)for word in sentences]
        tagged_sentence = [words for words in tokenized_sentences]
        
        return tagged_sentence
    

def TOPIC_TAGGED_DF(df):
    all_topic=GET_ALL_TOPIC_NAMES_FROM_TOPIC(topic)
    for word in all_topic:
        for row_num,text in enumerate(df['Noun']):
            
            c=0
            text_mod = re.sub(' +',' ',text)
            tagged_sentences = TOPIC_TAGGING_FUNCTION(text_mod)
            for sentence in tagged_sentences:
                for word_tag in sentence:
                    #print word_tag
                    #if word_tag == word or word.startswith(word_tag[0:len(word_tag)-1]) :
                    if (word_tag == word or SnowballStemmer("english").stem(word_tag) ==word
                        or SnowballStemmer("porter").stem(word_tag)) :
                        c=c+1
            
            df.loc[row_num,word] = c  
    return df


path = 'D:/star/8 emotions/YHM/Synopsis_Topics/3 topics'
extension = 'csv'
os.chdir(path)


files=[i for i in glob.glob('*.{}'.format(extension))  if i.find('Topic')>-1]

# GET THE MASTER DATA FRAME

master_df=pd.read_csv('D:/star/8 emotions/YHM/YHM_SYNOPSIS_tagged.csv')
master_df['TXDate']=pd.to_datetime(master_df['TXDate']).dt.strftime('%d/%m/%Y')
master_df['TXDate']=pd.to_datetime(master_df.TXDate) 

# CLEAN THE NOUN DATA 

master_df['Synopsis']=master_df.Synopsis.apply(REMOVE_SPECIAL_CHARS)
master_df['Noun']=master_df.Noun.apply(REMOVE_SPECIAL_CHARS)

# GET TOPIC DATA FRAME
location_variable='D:/star/8 emotions/YHM/Synopsis_Topics/Word_count_synopsis'



for file_name in files:
     
    final_file_to_export_name=location_variable+'/'+file_name
    file_name=files[1]
    # CREATE TOPIC DATA FRAME
    topic=TOPIC_DF(file_name)
    # FILTER THE MASTER DATA BASED ON TOPIC DATA DATE 
    master_df=FILTER_MASTER_DATA_WITH_DATE(file_name,master_df)
    # RUN  THE COUNT ALGORITHM
    temp_final_df=TOPIC_TAGGED_DF(master_df)
    temp_final_df_melted=pd.melt(temp_final_df, id_vars=
                                 ['Synopsis','Noun','TXDate'], var_name=['vals'])
    # EXPORT TO DF
    temp_final_df_melted.to_csv(final_file_to_export_name,index=False)
    
    
    

                               


   
    
