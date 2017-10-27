import pandas as pd
import re
import warnings
import os
import numpy as np
import glob
#extension = 'csv'
def CLEAN_PAIRS(x):
    x=x.replace('-P-','')
    return re.sub('[^a-zA-Z_]+', '', x)
def CLEAN_CHARS(x):
    x=x.replace('-C-','')
    return re.sub('[^a-zA-Z_]+', '', x)
def CLEAN_EMOTIONS(x):
    x=x.replace('-E-','')
    return re.sub('[^a-zA-Z_]+', '', x)

def CHAR_CHOOSE_FILTER(x):
    if '_' in x:
        return 'pair'
    else:
        return 'char'
def PAIRS_NEW(x):
    imp_pair=pairs_top
    if x not in imp_pair:
        return 'others_pair'
    else :
        return x

def CHARS_NEW(x):
    imp_char=chars_top
    if x not in imp_char:
        return 'others_char'
    else :
        return x         
""""""""""""""""""""" PAIRS DATA CREATION """""""""""""""

def PAIR_DATA_CREATION(share_for_show_data):

        df=pd.read_csv('PAIRS.csv')
        df.fillna(0,inplace=True)
        pair_melt=df.melt(id_vars=['Date'],var_name='pair',value_name='value')
        pair_melt['Date']=pd.to_datetime(pair_melt['Date']).dt.strftime('%d/%m/%Y')
        pair_melt['Date']=pd.to_datetime(pair_melt.Date)
        #pair_melt['month']=pair_melt['Date'].dt.month
        pair_melt['year']=pair_melt['Date'].dt.year
        pairs_grouped_yearly=pair_melt.groupby(['year','pair'])['value'].sum().reset_index()
        pairs_grouped_yearly_all=pair_melt.groupby(['year'])['value'].sum().reset_index()
        pairs_grouped_joined=pairs_grouped_yearly.merge(pairs_grouped_yearly_all,on='year',how='inner')
        pairs_grouped_joined.rename(columns={'value_x':'monthly_pair_value','value_y':'individual_value'},
                             inplace=True)
    
        pairs_grouped_joined['percent_contribution']=pairs_grouped_joined['monthly_pair_value'].divide(
        pairs_grouped_joined.individual_value)*100
        test=pairs_grouped_joined.sort_values(['year','percent_contribution'],
                                              ascending=[True,False]).reset_index().drop('index',axis=1)
        test['pair']=test.pair.apply(CLEAN_PAIRS)   
        test=test[(test['percent_contribution']>0)]
        top5_pair=test.groupby('year').head(5).reset_index(drop=True)
        pairs_top=list(top5_pair.pair.unique())
        global pairs_top
        del(df,pair_melt,pairs_grouped_yearly,pairs_grouped_yearly_all,pairs_grouped_joined,test,
            top5_pair)
        """"""" CONTRIBUTION STARTS """""""
        df=pd.read_csv('PAIRS.csv')
        df.fillna(0,inplace=True)
        pair_melt=df.melt(id_vars=['Date'],var_name='pair',value_name='value')
        pair_melt['Date']=pd.to_datetime(pair_melt.Date)
        pair_melt['month']=pair_melt['Date'].dt.month
        pair_melt['year']=pair_melt['Date'].dt.year
        pair_melt['pair']=pair_melt.pair.apply(CLEAN_PAIRS)
		  #### UPDATE THE PAIRS_NEW FUNCTION HERE ####
        pair_melt['pair']=pair_melt.pair.apply(PAIRS_NEW)
        pairs_grouped=pair_melt.groupby(['year','month','pair'])['value'].mean().reset_index()
        pairs_grouped_values=pairs_grouped.groupby(['year','month'])['value'].sum().reset_index()
        pairs_grouped_full=pairs_grouped_values.merge(pairs_grouped,on=['year','month'],how='inner')
        pairs_grouped_full.rename(columns={'value_x':'monthly_pair_value','value_y':'individual_value'},
							 inplace=True)
        
        pairs_grouped_full['percent_contribution']=pairs_grouped_full['individual_value'].divide(
		  pairs_grouped_full.monthly_pair_value)*100
        unique_pairs=list(pairs_grouped_full.pair.unique())
        global unique_pairs
        for i in unique_pairs:
            print i 
            t_df=pairs_grouped_full[(pairs_grouped_full['pair']==i)]
            t_df=t_df[['percent_contribution','month','year']]
            t_df['char_contri']=t_df.percent_contribution
            t_df['sd_half_con']=t_df.char_contri.mean()+ 0.5*(t_df.char_contri.std())
            t_df['char']=i
            if ( (i==unique_pairs[0]) ):
                    master=t_df
            else:
                master=master.append(t_df,ignore_index=True)
                
        master.drop('percent_contribution',axis=1,inplace=True)
        master.rename(columns={'char_contri':'feature_contribution','sd_half_con':'threshold',
                               'char':'feature'},inplace=True)
        
        master['feature_peak'] = np.where(master['feature_contribution']>master['threshold'], 
                                           1,0)
        master['Identifier']='Pair'
        share_for_show_data_df=pd.read_csv('D:/star/tvr/shares/new_shares_normalised/'+
                                           share_for_show_data+'.csv')
        share_for_show_data_df=share_for_show_data_df[['Date','month','year','Normalised Share']]
        share_for_show_data_df.drop_duplicates(subset=['year','month'], keep="last",inplace=True)
        """ join share data with master"""
#        master2=master.merge(share_for_show_data_df,on=['year','month'],how='inner')
        master.to_csv('pair_conti.csv',index=False)
    

""""""""""""""""""""" CHAR DATA CREATION """""""""""""""

def CHAR_DATA_CREATION(share_for_show_data):
    
        """ YEARLY CONTRIBUTION """
        df=pd.read_csv('CHARACTERS.csv')
        df.fillna(0,inplace=True)
        char_melt=df.melt(id_vars=['Date'],var_name='char',value_name='value')
        char_melt['Date']=pd.to_datetime(char_melt['Date']).dt.strftime('%d/%m/%Y')
        char_melt['Date']=pd.to_datetime(char_melt.Date)
        char_melt['year']=char_melt['Date'].dt.year
        char_melt['month']=char_melt['Date'].dt.month
        chars_grouped_yearly=char_melt.groupby(['year','char'])['value'].sum().reset_index()
        chars_grouped_yearly_all=char_melt.groupby(['year'])['value'].sum().reset_index()
        chars_grouped_joined=chars_grouped_yearly.merge(chars_grouped_yearly_all,on='year',how='inner')
        chars_grouped_joined.rename(columns={'value_x':'monthly_pair_value','value_y':'individual_value'},
                             inplace=True)
    
        chars_grouped_joined['percent_contribution']=chars_grouped_joined['monthly_pair_value'].divide(
        chars_grouped_joined.individual_value)*100
        test=chars_grouped_joined.sort_values(['year','percent_contribution'],
                                              ascending=[True,False]).reset_index().drop('index',axis=1)
        test['char']=test.char.apply(CLEAN_CHARS)        
        top5_char=test.groupby('year').head(5).reset_index(drop=True)
        chars_top=list(top5_char.char.unique())
        global chars_top
        #pd.DataFrame(chars_top).to_csv('chars_top.csv',index=False)
        #top5_char.to_csv('top_5_char_desc.csv',index=False)
        #pd.DataFrame(chars_top).to_csv('top_5_char.csv',index=False)
        del(df,char_melt,chars_grouped_yearly,chars_grouped_yearly_all,chars_grouped_joined,test,
            top5_char)
        df=pd.read_csv('CHARACTERS.csv')
        df.fillna(0,inplace=True)
        char_melt=df.melt(id_vars=['Date'],var_name='chars',value_name='value')
        char_melt['Date']=pd.to_datetime(char_melt['Date']).dt.strftime('%d/%m/%Y')
        char_melt['Date']=pd.to_datetime(char_melt.Date)
        char_melt['month']=char_melt['Date'].dt.month
        char_melt['year']=char_melt['Date'].dt.year
        char_melt['chars']=char_melt.chars.apply(CLEAN_CHARS)
		  #### UPDATE THE PAIRS_NEW FUNCTION HERE ####
        char_melt['chars']=char_melt.chars.apply(CHARS_NEW)
        chars_grouped=char_melt.groupby(['year','month','chars'])['value'].mean().reset_index()
        chars_grouped_values=chars_grouped.groupby(['year','month'])['value'].sum().reset_index()
        chars_grouped_full=chars_grouped_values.merge(chars_grouped,on=['year','month'],how='inner')
        chars_grouped_full.rename(columns={'value_x':'monthly_pair_value','value_y':'individual_value'},
							 inplace=True)
        chars_grouped_full['percent_contribution']=chars_grouped_full['individual_value'].divide(
		  chars_grouped_full.monthly_pair_value)*100
        unique_chars=list(chars_grouped_full.chars.unique())
        for i in unique_chars:
            print i 
            t_df=chars_grouped_full[(chars_grouped_full['chars']==i)]
            t_df=t_df[['percent_contribution','month','year']]
            t_df['char_contri']=t_df.percent_contribution
            t_df['sd_half_con']=t_df.char_contri.mean()+ 0.5*(t_df.char_contri.std())
            t_df['char']=i
            if ( (i==unique_chars[0]) ):
                    master=t_df
            else:
                master=master.append(t_df,ignore_index=True)
                
        master.drop('percent_contribution',axis=1,inplace=True)
        master.rename(columns={'char_contri':'feature_contribution','sd_half_con':'threshold',
                               'char':'feature'},inplace=True)
        
        master['feature_peak'] = np.where(master['feature_contribution']>master['threshold'], 
                                           1,0)
        master['Identifier']='Individual'
        master.to_csv('char_conti.csv',index=False)        
        
def CHAR_PAIR_EMO(share_for_show_data):
        
        char_pair_emo_df=pd.read_csv('emo_pair_'+share_for_show_data+'.CSV')
        char_pair_emo_df=char_pair_emo_df[['char','date','emotion','value','month','year']]
        #char_pair_emo_df['date']=pd.to_datetime(char_pair_emo_df['date']).dt.strftime('%d/%m/%Y')
        #char_pair_emo_df['date']=pd.to_datetime(char_pair_emo_df.date)
        #char_pair_emo_df['month']=char_pair_emo_df['date'].dt.month
        #char_pair_emo_df['year']=char_pair_emo_df['date'].dt.year
        char_pair_emo_df['char_pair']=char_pair_emo_df.char.apply(CHAR_CHOOSE_FILTER)
        
        """ PAIR EMOTION COMBINATION """
        # keep only share of pairs     
        pairs_df=char_pair_emo_df[  char_pair_emo_df['char_pair']=='pair' ]
        pairs_df['new_pair']=pairs_df.char.apply(PAIRS_NEW)
        # ROLLING THE DATA AT MONTHLY LEVEL
        pairs_emo_grouped_share2=pairs_df.groupby(['year','month','new_pair','emotion'])['value'].mean().reset_index()
        emo=pairs_emo_grouped_share2.groupby(['year','month','emotion'])['value'].sum().reset_index()
        emo_pair=emo.merge(pairs_emo_grouped_share2,on=['year','month','emotion'],how='inner')
        emo_pair.rename(columns={'value_x':'monthly_emo_value','value_y':'individual_value'},inplace=True)
        emo_pair['percent_contribution']=emo_pair['individual_value'].divide(emo_pair.monthly_emo_value)*100
        emo_pair['pair_emo']=emo_pair['new_pair']+'_'+emo_pair['emotion']
        
        emotions_to_get=['anger','disgust','fear','joy','sadness','surprise']
        unique_pairs=list(pairs_emo_grouped_share2.new_pair.unique())
        for i in unique_pairs:
            for j in emotions_to_get:
                t_df=emo_pair[ (emo_pair['new_pair']==i) & (emo_pair['emotion']==j)]
                t_df=t_df[['percent_contribution','month','year']]
                t_df['char_contri']=t_df['percent_contribution']
                #t_df$sd_half_con=mean(t_df$char_contri)+0.5*sd(t_df$char_contri)
                t_df['sd_onehalf_con']=t_df.char_contri.mean()+ 1.5 * t_df.char_contri.std()
                t_df['char_pair']=i+"_"+j
                if ((i==unique_pairs[0]) & (j==emotions_to_get[0])) :
                    master=t_df
                else:
                    master=master.append(t_df,ignore_index=True)
        master.drop('percent_contribution',axis=1,inplace=True)
        master.rename(columns={'char_contri':'pair_emo_contribution'},inplace=True)
        master.rename(columns={'char_contri':'feature_contribution','sd_onehalf_con':'threshold',
                               'char_pair':'feature'},inplace=True)
        
        master['feature_peak'] = np.where(master['feature_contribution']>master['threshold'], 
                                           1,0)
        master['Identifier']='Pair_emotion'        
        master.to_csv('pair_emo_contri.csv',index=False)
    
        """ CHARACTER EMOTION COMBINATION """
        char_df=char_pair_emo_df[  char_pair_emo_df['char_pair']=='char' ]
        char_df['new_char']=char_df.char.apply(CHARS_NEW)
        # ROLLING THE DATA AT MONTHLY LEVEL
        #emo_grouped_sum=pairs_df.groupby(['year','month','emotion'])['value'].sum().reset_index()
        char_emo_grouped_share2=char_df.groupby(['year','month','new_char','emotion'])['value'].mean().reset_index()
        emo=char_emo_grouped_share2.groupby(['year','month','emotion'])['value'].sum().reset_index()
        emo_char=emo.merge(char_emo_grouped_share2,on=['year','month','emotion'],how='inner')
        emo_char.rename(columns={'value_x':'monthly_emo_value','value_y':'individual_value'},inplace=True)
        emo_char['percent_contribution']=emo_char['individual_value'].divide(emo_char.monthly_emo_value)*100
        unique_chars=list(char_emo_grouped_share2.new_char.unique())
        del(master,tdf,t_df)
        for i in unique_chars:
           for j in emotions_to_get:
               t_df=emo_char[ (emo_char['new_char']==i) & (emo_char['emotion']==j)]
               t_df=t_df[['percent_contribution','month','year']]
               t_df['char_contri']=t_df['percent_contribution']
               #t_df$sd_half_con=mean(t_df$char_contri)+0.5*sd(t_df$char_contri)
               t_df['sd_onehalf_con']=t_df.char_contri.mean()+ 1.5 * t_df.char_contri.std()
               t_df['char_pair']=i+"_"+j
               if ((i==unique_chars[0]) & (j==emotions_to_get[0])) :
                   master=t_df
               else:
                   master=master.append(t_df,ignore_index=True)
        master.drop('percent_contribution',axis=1,inplace=True)
        master.rename(columns={'char_contri':'char_emo_contribution'},inplace=True)
        master.rename(columns={'char_contri':'feature_contribution','sd_onehalf_con':'threshold',
                               'char_pair':'feature'},inplace=True)
        
        master['feature_peak'] = np.where(master['feature_contribution']>master['threshold'], 
                                           1,0)      
        master['Identifier']='Individual_emotion'
        master.to_csv('char_emo_contri.csv',index=False)

      

""" FOLDER PATH NAME """
shows_folder_path = 'C:/Users/User/Desktop/All shows data/Joined old and new'
root, shows_path_directory, files= os.walk(shows_folder_path).next()
""" TVR AND SHARE DATA PATH NAME """
share_data_file_path='D:/star/tvr/shares/new_shares_normalised'
extension = 'csv'
os.chdir(share_data_file_path)
files_share_data = [i.replace('.csv','') for i in glob.glob('*.{}'.format(extension))]
all_show_names=list(set(shows_path_directory)-(set(shows_path_directory)-set(files_share_data)))
#pairs_create,emotions_create,chars_create
for show_number,show in enumerate(all_show_names):
    os.chdir('C:/Users/User/Desktop/All shows data/Joined old and new/'+show+'/new features/')
    #destination='C:/Users/User/Desktop/All shows data/Joined old and new/'+show+'/'
    print os.getcwd()
    print show_number+1
    #warnings.filterwarnings('ignore')
    #PAIR_DATA_CREATION(show)
    CHAR_DATA_CREATION(show)



####################################################################################

            

