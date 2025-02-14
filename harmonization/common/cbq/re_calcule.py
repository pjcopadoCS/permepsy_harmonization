import os
import math
import numpy as np
import pandas as pd

def filter(df,dataset,items,range_items):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    items = pre_items + post_items
    range_items = range_items + range_items
    
    df = df[df['database_0']==dataset][items]
    for indx,row in df.iterrows():
        for indy,k in enumerate(row.keys()):
            try:
                if math.isnan(row[k]):
                    df.loc[indx,k] = pd.NA
                elif (row[k] not in range_items[indy]):
                    df.loc[indx,k] = pd.NA
            except:
                df.loc[indx,k] = pd.NA
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
    I = [1,3,20,22,23,28]
    C = [2,4,7,10,12,25]
    DT = [5,11,14,15,27,30]
    JTC = [6,9,17,18,21,29]
    ER = [8,13,16,19,29,26]
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

    o_item = [preffix+'_'+item+"_0" for item in items]
    f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]
    r_item = [I,C,DT,JTC,ER,range(1,31)]

    for indx,row in df.iterrows():

        for indy,t in enumerate(r_item):
            col = [o_item[i-1] for i in t]
            try:
                df.loc[indx,f_item[indy]] = row[col].sum(min_count=len(col))
            except:
                df.loc[indx,f_item[indy]] = pd.NA

    ret = o_item + f_item
    return df,ret

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    
    print("NEW WAY")
    
    items =['CBQ_1','CBQ_2','CBQ_3','CBQ_4','CBQ_5','CBQ_6','CBQ_7','CBQ_8','CBQ_9','CBQ_10','CBQ_11','CBQ_12','CBQ_13','CBQ_14','CBQ_15','CBQ_16','CBQ_17','CBQ_18','CBQ_19','CBQ_20','CBQ_21','CBQ_22','CBQ_23','CBQ_24','CBQ_25','CBQ_26','CBQ_27','CBQ_28','CBQ_29','CBQ_30']
    n_items = ['CBQ_I', 'CBQ_C','CBQ_DT', 'CBQ_JTC', 'CBQ_ER', 'CBQ_T']
    
    range_items = [range(1,4)]*30
    range_items_n = [(6,18),(6,18),(6,18),(6,18),(6,18),(30,91)]
    
    df = filter(df,dataset,items,range_items)
    print("Previous dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    try:
        
        total_items = []
        df,it = calcule('pre',df,dataset,var,items,n_items)
        total_items += it
        df,it = calcule('post',df,dataset,var,items,n_items)
        total_items += it
        
    except Exception as e:
        print(f"Error in rule {var} {dataset}: ",e)
	
    df = df[total_items]
    print("Final dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)

    print("================End of harmonization=====================")
