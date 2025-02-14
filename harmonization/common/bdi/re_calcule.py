import os
import numpy as np
import pandas as pd

def filter(df,dataset,items,range_items,range_items_n):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    items = pre_items + post_items
    
    df = df[df['database_0']==dataset][items]
    for indx,row in df.iterrows():
        for indy,k in enumerate(row.keys()):
            try:
                if (row[k] not in range_items[indy]) and (not np.isnan(row[k])):
                    df.loc[indx,k] = pd.NA
            except:
                df.loc[indx,k] = pd.NA
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
        
	print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

	o_item = [preffix+'_'+item+"_0" for item in items]
	f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]
	r_item = [(0,21)]

	for indx,row in df.iterrows():

		for indy,t in enumerate(r_item):
			l,u = t
			try:
				df.loc[indx,f_item[indy]] = row[o_item[l:u]].sum(min_count=len(o_item[l:u]))
			except:
				df.loc[indx,f_item[indy]] = pd.NA
 
	ret = o_item + f_item
	return df,ret

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ["BDI_1", "BDI_2", "BDI_3", "BDI_4", "BDI_5","BDI_6", "BDI_7", "BDI_8", "BDI_9", "BDI_10", "BDI_11", "BDI_12", "BDI_13", "BDI_14", "BDI_15", "BDI_16", "BDI_17", "BDI_18", "BDI_19", "BDI_20", "BDI_21"]
    n_items = ["BDI_tot"]
    
    range_items = [range(4)]*21*2
    range_items_n = [range(0,64)]*2 
    
    df = filter(df,dataset,items,range_items,range_items_n)
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
