import os
import pandas as pd

def filter(df,dataset,items):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    items = pre_items + post_items
    
    df = df[df['database_0']==dataset][items]
    #df.replace(99,pd.NA,inplace=True)
    df.fillna(pd.NA,inplace=True)
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

    o_items = [preffix+'_'+item+"_0" for item in items]
    f_items = [preffix+'_'+n_item+"_0" for n_item in n_items]

    df[f_items] = 0
    for indx,row in df.iterrows():
        try:
            aggre = row[o_items].sum(min_count=len(o_items))
            df.loc[indx,f_items[0]]= 1 if aggre <= 20 else 0 
        except Exception as e:
            df.loc[indx,f_items[0]] = pd.NA

    r = f_items
    return df,r

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ["BDI_1", "BDI_2", "BDI_3", "BDI_4", "BDI_5","BDI_6", "BDI_7", "BDI_8", "BDI_9", "BDI_10", "BDI_11", "BDI_12", "BDI_13", "BDI_14", "BDI_15", "BDI_16", "BDI_17", "BDI_18", "BDI_19", "BDI_20", "BDI_21"]
    n_items = ["Depression"]
    
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