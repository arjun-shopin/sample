import pandas as pd
import re
import warnings
import os
#import numpy as np
os.chdir('C:/Users/Admin/Desktop/ISHQBAZ')
warnings.filterwarnings('ignore')

share=pd.read_excel('C:/Users/User/Downloads/YHM Trend.xlsx')
    
var = int(raw_input("Press 1 to apply for all chars else 0 for creating other chars: "))    
if var ==1:
    print 'Running for all characters'
else :
    print 'Running for filtered set'

CORR=True
CONTRIBUTION=True

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
    
    if var == 0 :
        imp_pair=['Ishita_Raman','Raman_Shagun','Ishita_Shagun','Ishita_Ruhi','Raman_Ruhi','Ashok_Raman',
                  'Ishita_Pihu','Raman_Pihu','Ashok_Pihu','Ruhi_Pihu']
        if x not in imp_pair:
            return 'others_pair'
        else :
            return x
    else :
        #print "No character filter applied " 
        return x
    
def CHAR_NEW(x):
    if var == 0 :
        imp_char=['Ishita','Raman','Shagun','Ruhi','Ashok','Pihu']
        if x not in imp_char:
            return 'others_char'
        else :
            return x  
    else :
        return x
####################################################################################
        
""""""""""""""""""""" PAIRS DATA CREATION """""""""""""""

def PAIR_DATA_CREATION():

    df=pd.read_csv('PAIRS.csv')
    # CREATE MONTH AND YEAR VAR 
    df['Date']=pd.to_datetime(df.Date)
    df['month']=df['Date'].dt.month
    df['year']=df['Date'].dt.year
    pair_melt=df.melt(id_vars=['Date','month','year'],var_name='pair',value_name='value')
    pair_melt['pair']=pair_melt.pair.apply(CLEAN_PAIRS)
    pair_melt['pair']=pair_melt.pair.apply(PAIRS_NEW)
    pairs_grouped=pair_melt.groupby(['year','month','pair'])['value'].mean().reset_index()
    pairs_grouped_values=pairs_grouped.groupby(['year','month'])['value'].sum().reset_index()
    pairs_grouped_full=pairs_grouped_values.merge(pairs_grouped,on=['year','month'],how='inner')
    pairs_grouped_full.rename(columns={'value_x':'monthly_pair_value','value_y':'individual_value'},
                         inplace=True)

    pairs_grouped_full['percent_contribution']=pairs_grouped_full['individual_value'].divide(
    pairs_grouped_full.monthly_pair_value)*100
    # THREHOLDING CODE
    """ GET UNIQUE CHARACTERS FOR CONTRIBUTION """
    unique_pairs=list(pairs_grouped_full.pair.unique())
    if CONTRIBUTION:
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
        master.to_csv('pair_contri.csv',index=False)
        """"""""""""""""""" CORRELATION """""""""""""    
    if CORR:        
        pair_corr1=pairs_grouped.pivot_table('value',['year','month'],'pair').reset_index()
        pair_corr2=pair_corr1.merge(share,on=['year','month'],how='inner')
        pair_df_corr_monthly=pd.DataFrame()
        for row_num,pair in enumerate(unique_pairs):
            temp_df=pair_corr2[[pair,'z_norm_monthly']]
            corr_val=temp_df.corr().iloc[0,1]
            pair_df_corr_monthly.loc[row_num,'metric']=pair
            pair_df_corr_monthly.loc[row_num,'cor_value']=corr_val
        
        pair_df_corr_monthly.to_csv('PAIRS_CORRELATION.csv',index=False)
#PAIR_DATA_CREATION()
####################################################################################
""""""""""""""""""""" CHAR DATA CREATION """""""""""""""

def CHAR_DATA_CREATION():
    
    df=pd.read_csv('CHARACTERS.csv')
    df['Date']=pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')
    df['Date']=pd.to_datetime(df.Date)
    df['month']=df['Date'].dt.month
    df['year']=df['Date'].dt.year
    char_melt=df.melt(id_vars=['Date','month','year'],var_name='char',value_name='value')
    char_melt['char']=char_melt.char.apply(CLEAN_CHARS)
    char_melt['char']=char_melt.char.apply(CHAR_NEW)
    char_grouped=char_melt.groupby(['year','month','char'])['value'].mean().reset_index()
    char_grouped_values=char_grouped.groupby(['year','month'])['value'].sum().reset_index()
    char_grouped_full=char_grouped_values.merge(char_grouped,on=['year','month'],how='inner')
    char_grouped_full.rename(columns={'value_x':'monthly_char_value','value_y':'individual_value'},inplace=True)

    char_grouped_full['percent_contribution']=char_grouped_full['individual_value'].divide(
            char_grouped_full.monthly_char_value)*100
    """ GET UNIQUE CHARACTERS FOR CONTRIBUTION """
    unique_chars=list(char_grouped_full.char.unique())
    if CONTRIBUTION:    
        for i in unique_chars:
            print i 
            t_df=char_grouped_full[(char_grouped_full['char']==i)]
            t_df=t_df[['percent_contribution','month','year']]
            t_df['char_contri']=t_df.percent_contribution
            t_df['sd_half_con']=t_df.char_contri.mean()+ 0.5*(t_df.char_contri.std())
            t_df['char']=i
            if ( (i==unique_chars[0]) ):
                master=t_df
            else:
                master=master.append(t_df,ignore_index=True)
        master.to_csv('char_contri.csv',index=False)
        
    """"""""""""""""""" CORRELATION """""""""""""
    if CORR:
        char_corr1=char_grouped.pivot_table('value',['year','month'],'char').reset_index()
        char_corr2=char_corr1.merge(share,on=['year','month'],how='inner')
        char_df_corr_monthly=pd.DataFrame()
        for row_num,char in enumerate(unique_chars):
            temp_df=char_corr2[[char,'z_norm_monthly']]
            corr_val=temp_df.corr().iloc[0,1]
            char_df_corr_monthly.loc[row_num,'metric']=char
            char_df_corr_monthly.loc[row_num,'cor_value']=corr_val
        char_df_corr_monthly.to_csv('CHAR_CORRELATION.csv',index=False)
####################################################################################
    
""""""""""""""""""""" EMOTIONS DATA CREATION """""""""""""""

def EMO_DATA_CREATION():
  
    df=pd.read_csv('EMOTIONS.csv')
    df['Date']=pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')
    df['Date']=pd.to_datetime(df.Date)
    df['month']=df['Date'].dt.month
    df['year']=df['Date'].dt.year
    emo_melt=df.melt(id_vars=['Date','month','year'],var_name='emo',value_name='value')
    emo_df_grouped=emo_melt.groupby(['year','month','emo'])['value'].sum().reset_index()
    emo_df_tot=emo_df_grouped.groupby(['year','month'])['value'].sum().reset_index()
    emo_final=emo_df_tot.merge(emo_df_grouped,on=['year','month'],how='inner')
    emo_final.rename(columns={'value_x':'monthly_emo_value','value_y':'individual_value'},inplace=True)
    emo_final['percent_contribution']=emo_final['individual_value'].divide(emo_final.monthly_emo_value)*100
    emo_final['emo']=emo_final['emo'].apply(CLEAN_EMOTIONS)
    master=pd.DataFrame()
    emotions_to_get=['anger','disgust','fear','joy','sadness','surprise']
    if CONTRIBUTION:
        for i in emotions_to_get:
            print i 
            t_df=emo_final[(emo_final['emo']==i)]
            t_df=t_df[['percent_contribution','month','year']]
            t_df['char_contri']=t_df.percent_contribution
            t_df['sd_half_con']=t_df.char_contri.mean()+ 0.5*(t_df.char_contri.std())
            t_df['emo']=i
            if ( (i==emotions_to_get[0]) ):
                master=t_df
            else:
                master=master.append(t_df,ignore_index=True)
        master.drop('percent_contribution',axis=1,inplace=True)
        master.rename(columns={'char_contri':'emo_contribution'})
        master.to_csv('EMO_CONTRIB.CSV',index=False)
        
    """"""""""""""""""" CORRELATION """""""""""""
    if CORR:
        emo_melt_gb_month=emo_melt.groupby(['year','month','emo'])['value'].mean().reset_index()    
        emo_monthly_mean=emo_melt_gb_month.pivot_table('value',['year','month'],'emo').reset_index()
        share_emo_month_joined=emo_monthly_mean.merge(share,on=['year','month'],how='inner')
        emo_df_corr_monthly=pd.DataFrame()
        #subbset df and run loop
        for row_num,emo in enumerate(emotions_to_get):
            temp_df=share_emo_month_joined[[emo,'z_norm_monthly']]
            corr_val=temp_df.corr().iloc[0,1]
            emo_df_corr_monthly.loc[row_num,'metric']=emo
            emo_df_corr_monthly.loc[row_num,'cor_value']=corr_val
            
        emo_df_corr_monthly.to_csv('EMO_CORRELATION.CSV',index=False)
    
####################################################################################
    
def CHAR_EMO_PAIR():
    
    if CONTRIBUTION:    
        char_pair_emo_df=pd.read_csv('new_emo_pair_char.CSV')
        char_pair_emo_df=char_pair_emo_df[['char','Date','emotion','value']]
        char_pair_emo_df['Date']=pd.to_datetime(char_pair_emo_df['Date']).dt.strftime('%d/%m/%Y')
        char_pair_emo_df['Date']=pd.to_datetime(char_pair_emo_df.Date)
        char_pair_emo_df['month']=char_pair_emo_df['Date'].dt.month
        char_pair_emo_df['year']=char_pair_emo_df['Date'].dt.year
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
                t_df=emo_pair[ (emo_pair['new_pair']==i) & (emo_pair['emotion']==i)]
                tdf=t_df[['percent_contribution','month','year']]
                t_df['char_contri']=t_df['percent_contribution']
                #t_df$sd_half_con=mean(t_df$char_contri)+0.5*sd(t_df$char_contri)
                t_df['sd_onehalf_con']=t_df.char_contri.mean+ 1.5 * t_df.char_contri.std
                t_df['char_pair']=i+j
                if ((i==unique_pairs[0]) & (j==emotions_to_get[0])) :
                    master=t_df
                else:
                    master=master.append(tdf,ignore_index=True)
    
    """"""""""""""""""" CORRELATION """""""""""""
    if CORR:
        pair_emo_corr1=pairs_emo_grouped_share2.pivot_table('value',['year','month'],'new_pair').reset_index()
        pair_emo_corr2=pair_emo_corr1.merge(share,on=['year','month'],how='inner')
        pair_emo_df_corr_monthly=pd.DataFrame()
        for row_num,char in enumerate(unique_pairs):
            temp_df=pair_emo_corr2[[char,'z_norm_monthly']]
            corr_val=temp_df.corr().iloc[0,1]
            pair_emo_df_corr_monthly.loc[row_num,'metric']=char
            pair_emo_df_corr_monthly.loc[row_num,'cor_value']=corr_val
        pair_emo_df_corr_monthly.to_csv('CHAR_CORRELATION.csv',index=False) 
    
    """ CHARACTER EMOTION COMBINATION """
    
    if  CONTRIBUTION:
        char_df=char_pair_emo_df[  char_pair_emo_df['char_pair']=='char' ]
        char_df['new_char']=char_df.char.apply(CHAR_NEW)
        # ROLLING THE DATA AT MONTHLY LEVEL
        #emo_grouped_sum=pairs_df.groupby(['year','month','emotion'])['value'].sum().reset_index()
        char_emo_grouped_share2=char_df.groupby(['year','month','new_char','emotion'])['value'].mean().reset_index()
        emo=char_emo_grouped_share2.groupby(['year','month','emotion'])['value'].sum().reset_index()
        emo_char=emo.merge(char_emo_grouped_share2,on=['year','month','emotion'],how='inner')
        emo_char.rename(columns={'value_x':'monthly_emo_value','value_y':'individual_value'},inplace=True)
        emo_char['percent_contribution']=emo_char['individual_value'].divide(emo_char.monthly_emo_value)*100
        unique_chars=list(char_emo_grouped_share2.new_char.unique())
    
        for i in unique_chars:
            for j in emotions_to_get:
                t_df=emo_char[ (emo_char['new_char']==i) & (emo_char['emotion']==i)]
                tdf=t_df[['percent_contribution','month','year']]
                t_df['char_contri']=t_df['percent_contribution']
                #t_df$sd_half_con=mean(t_df$char_contri)+0.5*sd(t_df$char_contri)
                t_df['sd_onehalf_con']=t_df.char_contri.mean+ 1.5 * t_df.char_contri.std
                t_df['char_pair']=i+j
                if ((i==unique_chars[0]) & (j==emotions_to_get[0])) :
                    master=t_df
                else:
                    master=master.append(tdf,ignore_index=True)
                
    """"""""""""""""""" CORRELATION """""""""""""
    if CORR:
        char_emo_corr1=char_emo_grouped_share2.pivot_table('value',['year','month'],'new_char').reset_index()
        char_emo_corr2=char_emo_corr1.merge(share,on=['year','month'],how='inner')
        char_emo_df_corr_monthly=pd.DataFrame()
        for row_num,char in enumerate(unique_chars):
            temp_df=char_emo_corr2[[char,'z_ norm_monthly']]
            corr_val=temp_df.corr().iloc[0,1]
            char_emo_df_corr_monthly.loc[row_num,'metric']=char
            char_emo_df_corr_monthly.loc[row_num,'cor_value']=corr_val
        char_emo_df_corr_monthly.to_csv('CHAR_CORRELATION.csv',index=False)    
