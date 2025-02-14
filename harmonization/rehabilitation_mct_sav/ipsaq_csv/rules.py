import harmonization.common.ipsaq.re_calcule as re

def harmonize(df,dataset,var):
	re.harmonize(df,dataset,var)


'''import os
import pandas as pd


def calcule(preffix,df,dataset,var,P,N):
    
    print("calculating aggragetes",dataset,var)
    
    columns = ['ipsaq_IP', 'ipsaq_IN', 'ipsaq_PP', 'ipsaq_PN', 'ipsaq_SP', 'ipsaq_SN', 'ipsaq_sesg_ext',
    'ipsaq_sesg_per']
    
    for column in columns:
        df[preffix+'_'+column+"_0"] = 0
    
    for _,row in df.iterrows():
        
        for i in range(1,33):
            
            suffix1 = 'I'
            if row[preffix+f"_ipsaq_{i}_0"] == 2:
                suffix1 = 'P'
            elif row[preffix+f"_ipsaq_{i}_0"] == 3:
                suffix1 = 'S'
            
            suffix2 = "P"    
            if i in N:
                suffix2 = "N"
            
            row[preffix+'_ipsaq_'+suffix1+suffix2+"_0"] += 1
            
    df[preffix+"_ipsaq_sesg_ext"+"_0"] = df[preffix+"_ipsaq_IP"+"_0"] - df[preffix+"_ipsaq_IN"+"_0"]
    df[preffix+"_ipsaq_sesg_per"+"_0"] = (df[preffix+"_ipsaq_PP"+"_0"] 
                                     +df[preffix+"_ipsaq_PN"+"_0"])/(df[preffix+"_ipsaq_PN"+"_0"] + df[preffix+"_ipsaq_SN"+"_0"])                   
    

def harmonize(df,dataset,var):

    items =pre_ipsaq_1,pre_ipsaq_2,pre_ipsaq_3,pre_ipsaq_4,pre_ipsaq_5,pre_ipsaq_6,pre_ipsaq_7,pre_ipsaq_8,pre_ipsaq_9,pre_ipsaq_10,pre_ipsaq_11,
    pre_ipsaq_12,pre_ipsaq_13,pre_ipsaq_14,pre_ipsaq_15,pre_ipsaq_16,pre_ipsaq_17,pre_ipsaq_18,pre_ipsaq_19,pre_ipsaq_20,pre_ipsaq_21,pre_ipsaq_22,
    pre_ipsaq_23,pre_ipsaq_24,pre_ipsaq_25,pre_ipsaq_26,pre_ipsaq_27,pre_ipsaq_28,pre_ipsaq_29,pre_ipsaq_30,pre_ipsaq_31,pre_ipsaq_32,pre_ipsaq_IP,
    pre_ipsaq_IN,pre_ipsaq_PP,pre_ipsaq_PN,pre_ipsaq_SP,pre_ipsaq_SN,pre_ipsaq_sesg_ext,pre_ipsaq_sesg_per,post_ipsaq_1,post_ipsaq_2,post_ipsaq_3,
    post_ipsaq_4,post_ipsaq_5,post_ipsaq_6,post_ipsaq_7,post_ipsaq_8,post_ipsaq_9,post_ipsaq_10,post_ipsaq_11,post_ipsaq_12,post_ipsaq_13,
    post_ipsaq_14,post_ipsaq_15,post_ipsaq_16,post_ipsaq_17,post_ipsaq_18,post_ipsaq_19,post_ipsaq_20,post_ipsaq_21,post_ipsaq_22,post_ipsaq_23,
    post_ipsaq_24,post_ipsaq_25,post_ipsaq_26,post_ipsaq_27,post_ipsaq_28,post_ipsaq_29,post_ipsaq_30,post_ipsaq_31,post_ipsaq_32,post_ipsaq_IP,
    post_ipsaq_IN,post_ipsaq_PP,post_ipsaq_PN,post_ipsaq_SP,post_ipsaq_SN,post_ipsaq_sesg_ext,post_ipsaq_sesg_per

    items = [item.strip()+"_0" for item in items.replace("\n","").split(",")]

    P = [1,4,5,7,8,11,14,15,16,20,22,25,26,29,31,32]
    N = [i for i in range(1,33) if i not in P]
    
    print(f"Harmonizing {var}...on {dataset}")

    dfp = df[df['database_0']==dataset][items]
    print(dfp.shape)
    dfp.fillna(-99,inplace=True)
    
    dfp.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    try:
        
        calcule('pre',dfp,dataset,var,P,N)
        calcule('post',dfp,dataset,var,P,N)
  
    except Exception as e:
        print("Error in harmonization: ",e)
	
    print(dfp.shape)
    
    pre_items = [w for w in items if 'pre' in w]
    post_items = [w for w in items if 'post' in w]
    
    dfp[pre_items+post_items].to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)
    #df.loc[df['database_0']==dataset,pre_items+post_items] = dfp.values

    print("================End of harmonization=====================")'''