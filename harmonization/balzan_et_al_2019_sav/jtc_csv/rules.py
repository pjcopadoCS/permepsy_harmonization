import os
import pandas as pd

def filter(df,dataset,items):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    items = pre_items + post_items
    
    df = df[df['database_0']==dataset][items]
    df.replace(99,pd.NA,inplace=True)
    df.fillna(pd.NA,inplace=True)
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")
    
    f_item = preffix+'_'+n_items[0]+"_0"
    r = [f_item]
    df[f_item] = 0
    for indx,row in df.iterrows():
        o_item = preffix+'_'+items[0]+"_0"
        try:
            df.loc[indx,f_item]= int(row[o_item])
        except Exception as e:
            df.loc[indx,f_item] = pd.NA
        '''try:
            df.iloc[indx,f_item] = 1 if row[o_item] <= 2 else 0
		except Exception as e:
      df.iloc[indx,f_item] = pd.NA'''
    
    return df,r

def harmonize(df,dataset,var):

    items = ['Jumping85_15','Jumping60_40','Jumping_afect']
    n_items = ["jtc"]
    
    df = filter(df,dataset,items)
    print("Previous dimension:",df.shape)
    
    
    print(f"Harmonizing {var}...on {dataset}")
    df.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    

    try:
        
        total_items = []
        df,it = calcule('pre',df,dataset,var,items,n_items)
        total_items += it
        df,it = calcule('post',df,dataset,var,items,n_items)
        total_items += it
        
  
    except Exception as e:
        print("Error in harmonization: ",e)
	
    df = df[total_items]
    print("Final dimension:",df.shape)
    
    df.to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)

    print("================End of harmonization=====================")