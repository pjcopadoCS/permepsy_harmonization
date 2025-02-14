from harmonization.common.psyrats import re_calcule as re

def harmonize(df,dataset,var):
    re.harmonize(df,dataset,var)
    
'''import os
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
            
    
    #df.replace(99,pd.NA,inplace=True)
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
	print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

	o_item = [preffix+'_'+item+"_0" for item in items]
	i=11
	f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]

	for indx,row in df.iterrows():
		
		try:
			df.loc[indx,f_item[0]]= row[o_item[:i]].sum(min_count=1)
		except Exception as e:
			df.loc[indx,f_item[0]] = pd.NA
   
		try:
			df.loc[indx,f_item[1]]= row[o_item[i:]].sum(min_count=1)
		except Exception as e:
			df.loc[indx,f_item[1]] = pd.NA
	
 
	ret = o_item + f_item
	return df,ret

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ['psy_al1', 'psy_al2', 'psy_al3', 'psy_al4', 'psy_al5', 'psy_al6', 'psy_al7', 'psy_al8', 'psy_al9', 'psy_al10', 'psy_al11','psy_del1', 'psy_del2', 'psy_del3', 'psy_del4', 'psy_del5', 'psy_del6']
    n_items = ["psy_altotal","psy_deltotal"]
    
    range_items = [range(0,5)]*17*2
    range_items_n = [range(0,11*4+1),range(0,6*4+1)]*2 
    
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
'''