import os
import math
import random
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


def reduce(df,dataset,items):
    
    items_n = list(set(item[:-2] for item in items))
    print("Total items:",items_n)
    
    for indx,row in df.iterrows():
        for item in items_n:
            re_items = [it for it in items if (item+'_1' == it) or (item+'_2' == it) or (item+'_3' == it)]
            try:
                if pd.isna(row[re_items].values).any():
                    raise Exception("Error")   
                max_value = row[re_items].max()
                max_indices = [i for i, v in enumerate(row[re_items].values) if v == max_value]
                pos = random.choice(max_indices)
                df.loc[indx,item+'_0'] = pos+1
            except Exception as e:
                df.loc[indx,item+'_0'] = pd.NA
    
    print("Reducing:",dataset)
    df.drop(columns=[k for k in items if not k.endswith('_0')],inplace=True)
    print("Total items net:",len(items_n))
                
    return df


def filter(df,dataset,items,range_items_n):
    
    pre_items = []
    post_items = []
    for j in range(5):
        pre_items.extend(['pre_'+i+'_'+str(j) for i in items])
        post_items.extend(['post_'+i+'_'+str(j) for i in items])
    
    items = pre_items + post_items
    
  
    range_items_n = range_items_n + range_items_n
    
    df = df[df['database_0']==dataset][[k for k in items if k in df.columns]]
    #for k in df.columns:
    #    print(k)
    df = reduce(df,dataset,items)

    print("Original dimension:",df.shape)  
    for indx,row in df.iterrows():
        for indy,k in enumerate(row.keys()):
            try:                
                if (row[k] not in range_items_n[indy]) or (pd.isna(row[k])):
                    df.loc[indx,k] = pd.NA
            except Exception as e:
                df.loc[indx,k] = pd.NA
    
    return df

    
def calcule(preffix,df,dataset,var,items,n_items):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")
    
    P = [1,4,5,7,8,11,14,15,16]#,20,22,25,26,29,31,32]
    #N = [i for i in range(1,33) if i not in P]
    N = [i for i in range(1,17) if i not in P]
 
    o_item = [preffix+'_'+item+"_0" for item in items]
    f_item = [preffix+'_'+n_item+"_0" for n_item in n_items]
    r_item = [[item for indx,item in enumerate(o_item) if (indx+1) in P],[item for indx,item in enumerate(o_item) if (indx+1) in N]]
    
    ff_item = []
    for indx,item in enumerate(f_item[:-2]):
        if indx % 2 == 0:
            ff_item.append([item])
        else:
            ff_item[-1].append(item)

    for indx,row in df.iterrows():
        
        for indy,item in enumerate(ff_item):
            
            try:
                item_P = [k for k in r_item[0] if row[k] == (indy+1)]
                if np.isnan([row[k] for k in r_item[0]]).any():
                    raise Exception("Error")
                df.loc[indx,item[0]] = len(item_P)
            except Exception as e:
                df.loc[indx,item[0]] = pd.NA
            
            try:
                item_N = [k for k in r_item[1] if row[k] == (indy+1)]
                if np.isnan([row[k] for k in r_item[1]]).any():
                    raise Exception("Error")
                df.loc[indx,item[1]] = len(item_N)
            except Exception as e:
                df.loc[indx,item[1]] = pd.NA
        
        try: 
            df.loc[indx,f_item[6]] = df.loc[indx,f_item[0]] - df.loc[indx,f_item[1]]
        except Exception as e:
            df.loc[indx,f_item[6]] = pd.NA
            
        try:
            df.loc[indx,f_item[7]] = (df.loc[indx,f_item[2]]+df.loc[indx,f_item[3]])/(df.loc[indx,f_item[3]] + df.loc[indx,f_item[5]])  
        except Exception as e:
            df.loc[indx,f_item[7]] = pd.NA

    ret = o_item + f_item
    return df,ret


def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ['ipsaq_1','ipsaq_2', 'ipsaq_3','ipsaq_4', 'ipsaq_5', 'ipsaq_6', 'ipsaq_7', 'ipsaq_8',
             'ipsaq_9','ipsaq_10','ipsaq_11','ipsaq_12','ipsaq_13','ipsaq_14','ipsaq_15','ipsaq_16']#,
             #'ipsaq_17','ipsaq_18','ipsaq_19','ipsaq_20','ipsaq_21','ipsaq_22','ipsaq_23','ipsaq_24',
             #'ipsaq_25','ipsaq_26','ipsaq_27','ipsaq_28','ipsaq_29','ipsaq_30','ipsaq_31','ipsaq_32']
             
    n_items = ['ipsaq_IP','ipsaq_IN','ipsaq_PP','ipsaq_PN','ipsaq_SP','ipsaq_SN','ipsaq_sesg_ext','ipsaq_sesg_per']
    
    range_items = [range(1,4)]*16
    #range_items_n = [range(0,11*4+1),range(0,6*4+1)]*2 
    
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
	
    extra = ['ipsaq_17','ipsaq_18','ipsaq_19','ipsaq_20','ipsaq_21','ipsaq_22','ipsaq_23','ipsaq_24',
             'ipsaq_25','ipsaq_26','ipsaq_27','ipsaq_28','ipsaq_29','ipsaq_30','ipsaq_31','ipsaq_32']
    pre_extra = ['pre_'+item+"_0" for item in extra]
    post_extra = ['post_'+item+"_0" for item in extra]
    
    total_items = total_items[:16] + pre_extra + total_items[16:16+8]+total_items[16+8:2*16+8]+post_extra+total_items[2*16+8:]
    df[pre_extra+post_extra] = pd.NA
    df = df[total_items]
    print("Final dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)

    print("================End of harmonization=====================")
