import harmonization.common.ipsaq.re_calcule_germans as re

def harmonize(df,dataset,var):
	re.harmonize(df,dataset,var)
 
''''import os
import numpy as np
import pandas as pd

def sorting_key(c,variables):

    pre = 0
    if c.startswith('pre_'):
        pre = len(variables)
    else:
        pre = 2*len(variables)

    tokens = c.split('_')
    
    if len(tokens) == 4:
        _,base,ind,dx = tokens
        return [pre,variables.index('_'.join([base,ind])),int(dx)]
    elif len(tokens) == 5:
        _,base,base2,base3,dx = tokens
        return [pre,variables.index('_'.join([base,base2,base3])),int(dx)]


def recover(df,dataset,var,items):
    
    total_items = []
    for preffix in ['pre','post']:
        for i in range(0,5):
            for item in items:
                colum = preffix+'_'+item+'_'+str(i)
                if colum in df.columns:
                    total_items.append(colum)
    
    df = df[df['database_0']==dataset][total_items]
    print(df.shape)
    print("Recovering",dataset,var)
    df.fillna(-99,inplace=True)
    
    df.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    reduce(df,dataset,var,total_items)
    
    return df,total_items

def reduce(df,dataset,var,items):
    
    items_n = list(set(item[:-2] for item in items))
    
    print(items)
    
    for indx,row in df.iterrows():
        for item in items_n:
            
            if row[item+'_0'] != -99:
                
                re_items = [it for it in items if item in it and it != item+'_0' and len(it) == len(item)+2 and it != item+'_4']
                pos = np.argmax(row[re_items].values)
                df.loc[indx,item+'_0'] = pos+1
    
    print("Reducing:",dataset,var)
                
    return df

def calcule(preffix,df,dataset,var,N):
    
    items_w_v = ['ipsaq_4','ipsaq_6','ipsaq_7','ipsaq_10','ipsaq_13','ipsaq_14','ipsaq_19','ipsaq_20','ipsaq_21','ipsaq_22','ipsaq_23',
                 'ipsaq_24','ipsaq_25','ipsaq_26','ipsaq_27']

    items_agg = ['ipsaq_IP', 'ipsaq_IN', 'ipsaq_PP', 'ipsaq_PN', 'ipsaq_SP', 'ipsaq_SN', 'ipsaq_sesg_ext','ipsaq_sesg_per']
    
    print("calculating aggragetes",dataset,var)
    
    items_agg = [preffix+'_'+item for item in items_agg]
    items_w_v = [preffix+'_'+item for item in items_w_v]
    items_r = [preffix+"_"+item for item in items if preffix+'_'+item not in items_w_v]
    
    for item in items_r:
        df[item] = -99
        df[item] = df[item].astype(int)
        
    for item in items_agg:
        df[item+'_0'] = 0
    
    for indx,row in df.iterrows():
        
        for item in items_w_v:
                
                suffix1 = 'I'
                if row[item+'_0'] == 2:
                    suffix1 = 'P'
                elif row[item+'_0'] == 3:
                    suffix1 = 'S'
                
                _,_,i = item.split('_')
                suffix2 = "P"    
                if int(i) in N:
                    suffix2 = "N"
                
                df.loc[indx,preffix+'_ipsaq_'+suffix1+suffix2+"_0"] += 1
                
    df[preffix+"_ipsaq_sesg_ext"+"_0"] = df[preffix+"_ipsaq_IP"+"_0"] - df[preffix+"_ipsaq_IN"+"_0"]
    df[preffix+"_ipsaq_sesg_per"+"_0"] = (df[preffix+"_ipsaq_PP"+"_0"] 
                                     +df[preffix+"_ipsaq_PN"+"_0"])/(df[preffix+"_ipsaq_PN"+"_0"] + df[preffix+"_ipsaq_SN"+"_0"])        
                   
def harmonize(df,dataset,var):
    
    items =ipsaq_1,ipsaq_2,ipsaq_3,ipsaq_4,ipsaq_5,ipsaq_6,ipsaq_7,ipsaq_8,ipsaq_9,ipsaq_10,ipsaq_11,ipsaq_12,ipsaq_13,ipsaq_14,
    ipsaq_15,ipsaq_16,ipsaq_17,ipsaq_18,ipsaq_19,ipsaq_20,ipsaq_21,ipsaq_22,ipsaq_23,ipsaq_24,ipsaq_25,ipsaq_26,ipsaq_27,ipsaq_28,
    ipsaq_29,ipsaq_30,ipsaq_31,ipsaq_32,ipsaq_IP,ipsaq_IN,ipsaq_PP,ipsaq_PN,ipsaq_SP,ipsaq_SN,ipsaq_sesg_per,ipsaq_sesg_ext
    
    items = [item.strip() for item in items.split(',')]
 
    P = [1,4,5,7,8,11,14,15,16,20,22,25,26,29,31,32]
    N = [i for i in range(1,33) if i not in P]
    
    print(f"Harmonizing {var}...on {dataset}")

    dfp,total_items = recover(df,dataset,var,items)   
    dfp = df[df['database_0']==dataset][pre+post]
    print(dfp.shape)

    dfp.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    try:
        calcule('pre',dfp,dataset,var,N)
        calcule('post',dfp,dataset,var,N)
  
    except Exception as e:
        print("Error in harmonization: ",e)
	
    print(dfp.shape)
    
    pre_items = [w for w in items if 'pre' in w]
    post_items = [w for w in items if 'post' in w]
    
    total_items = [it for it in total_items if it.endswith('_0')]
    
    total_items.sort(key=lambda x: sorting_key(x,items))
    
    dfp[total_items].to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)
    #df.loc[df['database_0']==dataset,pre_items+post_items] = dfp.values
    
    for it in total_items:
        #df.loc[df['database_0']==dataset,it].astype(int)
        df.loc[df['database_0']==dataset,it] = dfp[it].values  
    
    df.to_csv('output'+os.sep+"after_all_"+dataset+'_'+var+'.csv',index=False)
    print("================End of harmonization=====================")'''