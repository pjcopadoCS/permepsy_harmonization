import os
import numpy as np
import pandas as pd

def filter(df,dataset,items,range_items_n):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    items = pre_items + post_items
    range_items_n = range_items_n + range_items_n
    
    df = df[df['database_0']==dataset][items]
    for indx,row in df.iterrows():
        for indy,k in enumerate(row.keys()):
            try:
                if (row[k] not in range_items_n[indy]) and (not np.isnan(row[k])):
                    df.loc[indx,k] = pd.NA
            except:
                df.loc[indx,k] = pd.NA
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

    o_item = [preffix+'_'+item+"_0" for item in items]
    f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]
    r_item = [[0,2,3,4,5,7,11,13,14],[i for i in range(0,15) if i not in [0,2,3,4,5,7,11,13,14]],[0,2,3,4,5,7,11,13,14]]

    for indx,row in df.iterrows():
        for indy,t in enumerate(r_item):
            try:
                items = [item for i,item in enumerate(o_item) if i in t]
                if indy < 2:
                    df.loc[indx,f_item[indy]] = row[items].sum(min_count=len(items))
                else:
                    items_n = [item for item in o_item if item not in items]
                    df.loc[indx,f_item[indy]] = row[items].sum(min_count=len(items)) - row[items_n].sum(min_count=len(items_n))
            except:
                df.loc[indx,f_item[-1]] = pd.NA

    ret = o_item + f_item
    return df,ret

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ['BCIS_1','BCIS_2','BCIS_3','BCIS_4','BCIS_5','BCIS_6','BCIS_7','BCIS_8','BCIS_9','BCIS_10','BCIS_11','BCIS_12','BCIS_13','BCIS_14','BCIS_15']
    n_items = ['BCIS_reflex', 'BCIS_certez', 'BCIS_total']
    
    range_items = [range(0,5)]*15
    range_items_n = [range(0,4*9+1),range(0,4*6+1),range(-4*6,4*9+1)]
    
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
