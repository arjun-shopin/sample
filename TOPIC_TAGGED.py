import pandas as pd
import re
from nltk import sent_tokenize
from nltk import word_tokenize
import os
import glob

path = 'D:/star/8 emotions/YHM/Synopsis_Topics/3 topics'
extension = 'csv'
os.chdir(path)


files=[i for i in glob.glob('*.{}'.format(extension))  if i.find('Topic')>-1]


topic=pd.read_csv('Topic_2014_6.csv')
master_df=pd.read_csv('D:/star/8 emotions/YHM/YHM_SYNOPSIS_tagged.csv')

master_df['TXDate']=pd.to_datetime(master_df['TXDate']).dt.strftime('%d/%m/%Y')
master_df['TXDate']=pd.to_datetime(master_df.TXDate) 

# FILTER THE DATA FRAME

filtered_df=master_df[(master_df.TXDate.dt.month==6) & (master_df.TXDate.dt.year==2014) ]
master_df=filtered_df.reset_index()
master_df=master_df[['Synopsis','Noun','TXDate']]
# CLEAN THE NOUN DATA 
def REMOVE_SPECIAL_CHARS(text):
    text=str(text).replace('^^','')
    text=re.sub('[^a-zA-Z]+', ' ', text)
    return text
    #text.replace('episode','').replace('online','')

master_df['Synopsis']=master_df.Synopsis.apply(REMOVE_SPECIAL_CHARS)
master_df['Noun']=master_df.Noun.apply(REMOVE_SPECIAL_CHARS)

##############
topic1=list(str(topic['Topic 1']))
topic1=map(list, topic['Topic 1'])
topic2=list(str(topic['Topic 2']))
topic2=map(list, topic['Topic 2'])
topic3=list(str(topic['Topic 2']))
topic3=map(list, topic['Topic 3'])
topic1=[''.join(i) for i in topic1]
topic2=[''.join(i) for i in topic2]
topic3=[''.join(i) for i in topic3]

all_topic=topic1+topic2+topic3

    
#master_loc=master_df   
#master_df=master_df.drop_na()

def TOPIC_TAGGING_FUNCTION(text):
        
        sentences = sent_tokenize(text)
        tokenized_sentences = [word_tokenize(word)for word in sentences]
        tagged_sentence = [words for words in tokenized_sentences]
        
        return tagged_sentence
def TOPIC_TAGGED_DF(df):
    for word in all_topic:
        for row_num,text in enumerate(df['Noun']):
            
            c=0
            text_mod = re.sub(' +',' ',text)
            tagged_sentences = TOPIC_TAGGING_FUNCTION(text_mod)
            for sentence in tagged_sentences:
                for word_tag in sentence:
                    #print word_tag
                    if word_tag == word or word.startswith(word_tag[0:len(word_tag)-1]) :
                        c=c+1
            
            df.loc[row_num,word] = c  
    return df
T=TOPIC_TAGGED_DF(master_df)  
test=pd.melt(T, id_vars=['Synopsis','Noun','TXDate'], var_name=['vals'])
test.to_csv('count_words_2014_6.csv',index=False)       

        
#master_df.to_csv('match.csv')           

                               


   
    