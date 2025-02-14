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
            #print(k,row[k],range_items[indy],row[k] in range_items[indy])
            try:
                if math.isnan(row[k]):
                    df.loc[indx,k] = pd.NA
                elif row[k] not in range_items[indy]:
                    df.loc[indx,k] = pd.NA
            except:
                df.loc[indx,k] = pd.NA
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
	print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

	o_item = [preffix+'_'+item+"_0" for item in items]
	f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]

	'''for indx,row in df.iterrows():

		for indy,t in enumerate(r_item):
			l,u = t
			try:
				df.loc[indx,f_item[indy]] = row[o_item[l:u]].sum(min_count=1)
			except:
				df.loc[indx,f_item[indy]] = pd.NA'''
 
	ret = o_item # + f_item
	return df,ret

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ['gaf']
    
    range_items = [range(0,301)]
    
    df = filter(df,dataset,items,range_items)
    print("Previous dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    try:
        
        total_items = []
        df,it = calcule('pre',df,dataset,var,items,items)
        total_items += it
        df,it = calcule('post',df,dataset,var,items,items)
        total_items += it
        
    except Exception as e:
        print(f"Error in rule {var} {dataset}: ",e)
	
    df = df[total_items]
    print("Final dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)

    print("================End of harmonization=====================")