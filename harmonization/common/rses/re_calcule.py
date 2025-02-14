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
                if (row[k] not in range_items_n[indy]) or (np.isnan(row[k])):
                    df.loc[indx,k] = pd.NA
            except:
                df.loc[indx,k] = pd.NA
    return df
    

def calcule(preffix,df,dataset,var,items,n_items,inv=lambda x: x):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")
    
    o_item = [preffix+'_'+item+"_0" for item in items]
    f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]
    
    I = [2,5,6,8,9]
    r_item = [[i for i in range(10) if (i+1) in I],[i for i in range(10) if (i+1) not in I]]

    for indx,row in df.iterrows():
        df.loc[indx,f_item[0]] = 0
        for indy,t in enumerate(r_item):
            try:
                items = [item for i,item in enumerate(o_item) if i in t]
                if indy == 0:
                    for it in items:
                        if pd.isna(row[it]):
                            raise Exception("Error")
                        row[it] = inv(row[it])
                    df.loc[indx,f_item[0]] += row[items].sum(min_count=len(items))
                else:
                    df.loc[indx,f_item[0]] += row[items].sum(min_count=len(items))
            except:
                df.loc[indx,f_item[0]] = pd.NA

    ret = o_item + f_item
    return df,ret

def harmonize(df,dataset,var,inv=lambda x: x):
    
    print(f"Harmonizing {var}...on {dataset}")
    
    items = ['Rosen_1','Rosen_2','Rosen_3','Rosen_4','Rosen_5','Rosen_6','Rosen_7','Rosen_8','Rosen_9','Rosen_10']
    n_items = ['Rosen_total']
    
    range_items = [range(1,5)]*10
    #range_items_n = [range(0,4*9+1),range(0,4*6+1),range(-4*6,4*9+1)]
    
    df = filter(df,dataset,items,range_items)
    print("Previous dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    try:
        
        total_items = []
        df,it = calcule('pre',df,dataset,var,items,n_items,inv)
        total_items += it
        df,it = calcule('post',df,dataset,var,items,n_items,inv)
        total_items += it
        
    except Exception as e:
        print(f"Error in rule {var} {dataset}: ",e)
	
    df = df[total_items]
    print("Final dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)

    print("================End of harmonization=====================")
