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
                if (int(row[k]) not in range_items_n[indy]) and (not np.isnan(row[k])):
                    df.loc[indx,k] = pd.NA
            except:
                df.loc[indx,k] = pd.NA
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

    o_item = [preffix+'_'+item+"_0" for item in items]
    f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]
    # Here indicate which item sum to wich subscore
    # r_item = [[0,2,3,4,5,7,11,13,14],[i for i in range(0,15) if i not in [0,2,3,4,5,7,11,13,14]],[0,2,3,4,5,7,11,13,14]]
    # In this case we only one score
    r_item = [list(range(0,len(o_item)))]

    for indx,row in df.iterrows():
        for indy,t in enumerate(r_item):
            try:
                items = [item for i,item in enumerate(o_item) if i in t]
                df.loc[indx,f_item[indy]] = row[items].sum(min_count=len(items))
            except:
                df.loc[indx,f_item[-1]] = pd.NA

    ret = o_item + f_item
    return df,ret

def harmonize(df,dataset,var):
    
    
    #Customise to your needs
    print(f"Harmonizing {var}...on {dataset}")
    items = ['field1', 'field2', 'field3', 'field4', 'field5', 'field6']
    n_items = ['field_T']
    
    #Introduce item ranges
    range_items = [range(-10,10)]*len(items)
    range_items_n = [range(-10,100)]*len(n_items)
        
    
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
