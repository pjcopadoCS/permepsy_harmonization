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
    L = 81.0 
    U = 94.0
    print(f"Intevale of decision {L} and {U}")
    o_items = [preffix+'_'+item+"_0" for item in items]
    f_items = [preffix+'_'+n_item+"_0" for n_item in n_items]

    df[f_items[0]] = 0
    for indx,row in df.iterrows():
        try:
            qol_t = row[o_items].sum(min_count=len(o_items))
            if qol_t < L:
                df.loc[indx,f_items[0]]= 0
            elif qol_t <= U:
                df.loc[indx,f_items[0]]= 1
            else:
                df.loc[indx,f_items[0]]= 2
        except Exception as e:
            df.loc[indx,f_items[0]] = pd.NA

    r = f_items
    return df,r

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ['WHOQOL1', 'WHOQOL2', 'WHOQOL3', 'WHOQOL4', 'WHOQOL5', 'WHOQOL6', 'WHOQOL7', 'WHOQOL8', 'WHOQOL9', 'WHOQOL10', 'WHOQOL11', 'WHOQOL12', 'WHOQOL13', 'WHOQOL14', 'WHOQOL15', 'WHOQOL16', 'WHOQOL17', 'WHOQOL18', 'WHOQOL19', 'WHOQOL20', 'WHOQOL21', 'WHOQOL22', 'WHOQOL23', 'WHOQOL24', 'WHOQOL25', 'WHOQOL26']
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