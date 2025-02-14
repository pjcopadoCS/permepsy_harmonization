import harmonization.common.rses.re_calcule as re

def harmonize(df,dataset,var):
    re.harmonize(df,dataset,var)
    

'''import os
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
		for item in items:
			column = preffix+'_'+item+'_0'
			total_items.append(column)
    
	df = df[df['database_0']==dataset][total_items]
	print(df.shape)
	print("Recovering",dataset,var)
	df.fillna(-99,inplace=True)
 
	df = reduce(df,dataset,var)
    
	df.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
	return df,total_items

def reduce(df,dataset,var):
    
    print("Replacing value 5 with 4 in order to harmonize the data 0 - 4 scale",dataset,var)	
    df.replace(5,4,inplace=True)
    return df
    
def invert(df,dataset,var,items,I):
    print("inversion of items in",I,"Rule 5 - i",dataset,var)
    
    for item in items:
        
        _,_,i,_ = item.split("_")
        if int(i) in I:
            df[item] = 5 - df[item]
    
    return df
        

def calcule(preffix,df,dataset,var,items):
    
    print("calculating aggragetes Rosen_total",dataset,var)
    item_preffix = preffix+"_"+'Rosen_total_0'
    df[item_preffix] = 0
    df[item_preffix] = df[item_preffix].astype(int)
    
    for item in items:
        item_preffix = preffix+"_"+'Rosen_total_0'
        df[item_preffix] = df[item_preffix].astype(int)
        
    for indx,row in df.iterrows():
        
        s = 0
        for item in items:
            item_preffix = preffix+"_"+item+"_0"
            s += row[item_preffix]
            
        df.loc[indx,preffix+'_'+'Rosen_total_0'] = s
        
    return df
                      
                   
def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    
    items =Rosen_1,Rosen_2,Rosen_3,Rosen_4,Rosen_5,Rosen_6,Rosen_7,Rosen_8,Rosen_9,Rosen_10,Rosen_total
    items = [item.strip().replace("\n","") for item in items.split(',')]
    
    agg_items = ['Rosen_total']
    val_items = [item for item in items if item not in agg_items]
	
    Inv = [2,5,6,8,9]
        
    print(val_items)

    dfp,total_items = recover(df,dataset,var,val_items)
    #dfp = invert(dfp,dataset,var,total_items,Inv)
    dfp = df[df['database_0']==dataset][pre+post]
    print(dfp.shape)
    
    dfp.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    try:
        calcule('pre',dfp,dataset,var,items)
        calcule('post',dfp,dataset,var,items)
  
    except Exception as e:
        print("Error in harmonization: ",e)
	
    print(dfp.shape)
    
    total_items += ['pre_Rosen_total_0','post_Rosen_total_0']
    total_items.sort(key=lambda c: sorting_key(c,items))
    dfp[total_items].to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)
    
    return dfp
    print("================End of harmonization=====================")'''