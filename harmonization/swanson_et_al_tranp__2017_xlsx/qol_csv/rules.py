import os
import pandas as pd

def filter(df,dataset,items):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    items = pre_items + post_items
    
    df = df[df['database_0']==dataset][items]
    df.replace(999.0,pd.NA,inplace=True)
    df.fillna(pd.NA,inplace=True)
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")
    L = 51.94
    U = 65.70
    print(f"Intevale of decision {L} and {U}")
    o_items = [preffix+'_'+item+"_0" for item in items]
    f_items = [preffix+'_'+n_item+"_0" for n_item in n_items]

    df[f_items] = 0
    for indx,row in df.iterrows():
        try:
            qol_t = row[o_items].sum(min_count=len(o_items))
            #df.loc[indx,f_items[0]]= qol_t
            if qol_t < L:
                df.loc[indx,f_items[0]]= 0
            elif qol_t <= U:
                df.loc[indx,f_items[0]]= 1
            else:
                df.loc[indx,f_items[0]]= 2
        except Exception as e:
            df.loc[indx,f_items] = pd.NA

    r = f_items
    return df,r

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ['qlq1','qlq2','qlq3','qlq4','qlq5','qlq6','qlq7','qlq8','qlq9','qlq10','qlq11','qlq12','qlq13','qlq14','qlq15','qlq16','qlq17','qlq18']
    n_items = ["gen_qol"]
    
    df = filter(df,dataset,items)
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