import pandas as pd
import re
import string
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
yhm=pd.read_csv('ye_hai_mohabbatein.csv',encoding='utf-8')
df=yhm[ ['Synopsis','TXDate'] ]
df=df.drop_duplicates()
df=df.reset_index()
df=df[ ['Synopsis','TXDate'] ]
#df.to_csv('sdf.csv',index=False)

Remove=['Raman','Simmi','Ashok','Mihir','Bhalla','Vandu'
       ,'Niddhi','Ruhi','Bala','Amma','Mr.','Aaliya',
       'Mihika','Pihu','Mani','Ishita','Romi','Shagun','Sarika','Adi',
       'trisha','santosh','madhavi','pooja','param','is','ask','asks','become','becomes','was','be','been','had','has','have'
       ,'everything','everyone','anyone','anything','does','do','a','an','the',
       'and','are','want','wants','make','makes']


rx = '[' + re.escape(' '.join(Remove)) + ']'
# filter date 

stop = list(stopwords.words('english'))

def data_Tokenization(text):
        
        sentences = sent_tokenize(text)
        tokenized_sentences = [word_tokenize(word)for word in sentences]
        tagged_sentence = [words for words in tokenized_sentences]
        
        return tagged_sentence
    
     
def RM_STOPWORDS(dataframe):
    for row_num,text in enumerate(dataframe['Synopsis']):
        text_mod = re.sub(' +',' ',text)
        tagged_sentences = data_Tokenization(text=text_mod)
                
        temp_text = []
    
    ################################ NOUN TAGGING ##########################            
        for sentence in tagged_sentences:
            for word_tag in sentence:
                if word_tag  not in stop:
                    temp_text.append(word_tag)
                    
                    sent_mod = " ".join(temp_text)     
    
        dataframe.loc[row_num,"RMV_STP"] = sent_mod
       
    return dataframe
    
stp_wds=RM_STOPWORDS(df)


def data_TokenizationAndTagging(text):
        
        sentences = sent_tokenize(text)
        tokenized_sentences = [word_tokenize(word)for word in sentences]
        tagged_sentence = [pos_tag(words) for words in tokenized_sentences]
        
        return tagged_sentence

def create_data_with_nouns_N_verbs(dataframe):
        
    
        list_of_objects_to_keep_NN = ["NN","NNS"]
        list_of_objects_to_keep_VB = ["VB","VBZ","VBD","VBG","VBN","VBP"]
        list_of_objects_to_keep_PN=["NNP","NNPS"]
#        list_of_objects_to_keep_VB = ["VB","VBZ","VBD","VBG","VBN","VBP"]
#        list_of_objects_to_keep_ADJ=["JJ","JJR","JJS"]
        
        print 'working'
        
        for row_num,text in enumerate(dataframe['Synopsis']):
            
            print row_num
            text_mod = re.sub(' +',' ',text)
            tagged_sentences = data_TokenizationAndTagging(text=text_mod)
            
            temp_text_NN = []
            
            temp_text_VB = []
            
            temp_text_PN=[]
            
#            temp_text_ADJ = []
################################ NOUN TAGGING ##########################            
            for sentence in tagged_sentences:
    
                for word_tag in sentence:
                    
                    if word_tag[1] in list_of_objects_to_keep_NN:
                        
                         temp_text_NN.append(word_tag[0])
                         
                    if word_tag[1] in list_of_objects_to_keep_VB:
                        
                        temp_text_VB.append(word_tag[0])
                    
                    if word_tag[1] in list_of_objects_to_keep_PN:
                        
                        temp_text_PN.append(word_tag[0])
                         
                         
            sent_mod_NN = " ".join(temp_text_NN)     
            
                       
            dataframe.loc[row_num,"Noun"] = sent_mod_NN
            
            sent_mod_VB = " ".join(temp_text_VB)
            
            dataframe.loc[row_num,"Verb"] = sent_mod_VB
            
            sent_mod_PN = " ".join(temp_text_PN)
            
            dataframe.loc[row_num,"Proper_Noun"] = sent_mod_PN
            
            
            
            
            print row_num
       
        return dataframe
    
tdf=create_data_with_nouns_N_verbs(df)

tdf.to_csv('tag_f.csv',index=False,encoding='utf-8')

new_stop_words=list(tdf.Proper_Noun.unique())

def RM_PN(dataframe):
    for row_num,text in enumerate(dataframe['Synopsis']):
        text_mod = re.sub(' +',' ',text)
        tagged_sentences = data_Tokenization(text=text_mod)
                
        temp_text = []
    
    ################################ NOUN TAGGING ##########################            
        for sentence in tagged_sentences:
            for word_tag in sentence:
                if word_tag  not in   new_stop_words:
                    temp_text.append(word_tag)
                    
                    sent_mod = " ".join(temp_text)     
    
        dataframe.loc[row_num,"RMV_PN"] = sent_mod
       
    return dataframe
    
PN_removed=RM_STOPWORDS(df)












