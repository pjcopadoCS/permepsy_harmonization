import os
import numpy as np
import pandas as pd

def filter(df,dataset,items,range_items_n):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    
    items = pre_items + post_items
    range_items_n = range_items_n + range_items_n
    
    df = df[df['database_0']==dataset][items]
    df = df.astype(float)
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
    
    P = [1,4,5,7,8,11,14,15,16,20,22,25,26,29,31,32]
    N = [i for i in range(1,33) if i not in P]
 
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
    items = ['ipsaq_1','ipsaq_2','ipsaq_3','ipsaq_4','ipsaq_5','ipsaq_6','ipsaq_7','ipsaq_8','ipsaq_9',
             'ipsaq_10','ipsaq_11','ipsaq_12','ipsaq_13','ipsaq_14','ipsaq_15','ipsaq_16','ipsaq_17',
             'ipsaq_18','ipsaq_19','ipsaq_20','ipsaq_21','ipsaq_22','ipsaq_23','ipsaq_24','ipsaq_25',
             'ipsaq_26','ipsaq_27','ipsaq_28','ipsaq_29','ipsaq_30','ipsaq_31','ipsaq_32']
             
    n_items = ['ipsaq_IP','ipsaq_IN','ipsaq_PP','ipsaq_PN','ipsaq_SP','ipsaq_SN','ipsaq_sesg_ext','ipsaq_sesg_per']
    
    range_items = [range(1,4)]*32
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
	
    df = df[total_items]
    print("Final dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)

    print("================End of harmonization=====================")
