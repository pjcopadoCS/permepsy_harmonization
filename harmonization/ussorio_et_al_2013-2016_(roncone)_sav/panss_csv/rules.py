import harmonization.common.panss.re_filter as re

def harmonize(df,dataset,var):
    re.harmonize(df,dataset,var)

'''import os
import numpy as np
import pandas as pd

def filter(df,dataset,items,n_items,range_items,range_items_n):
    
    pre_items = ['pre_'+i+'_0' for i in items+n_items]
    post_items = ['post_'+i+'_0' for i in items+n_items]
    items = pre_items + post_items
    range_items = range_items + range_items_n + range_items + range_items_n
    
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
	r_item = [(0,8),(8,15),(15,31),(0,31)]

	for indx,row in df.iterrows():

		for indy,t in enumerate(r_item):
			l,u = t
			try:
				df.loc[indx,f_item[indy]] = row[o_item[l:u]].sum(min_count=1)
			except:
				df.loc[indx,f_item[indy]] = pd.NA
 
	ret = o_item + f_item
	return df,ret

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ['pannsp1','pannsp2','pannsp3','pannsp4','pannsp5','pannsp6','pannsp7','pannsn1','pannsn2','pannsn3','pannsn4','pannsn5','pannsn6','pannsn7','pannsg1','pannsg2','pannsg3','pannsg4','pannsg5','pannsg6','pannsg7','pannsg8','pannsg9','pannsg10','pannsg11','pannsg12','pannsg13','panssg14','panssg15','panssg16']
    n_items = ['panss_P','panss_N','panss_G','panss_T']
    
    range_items = [range(1,8)]*30
    range_items_n = [range(7,50),range(7,50),range(16,113),range(30,211)]
    
    df = filter(df,dataset,items,n_items,range_items,range_items_n)
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