def harmonize(df,dataset,var):
    pass

'''import os
import pandas as pd

def filter(df,dataset,items):
    
    pre_items = ['pre_'+i+'_0' for i in items]
    post_items = ['post_'+i+'_0' for i in items]
    items = pre_items + post_items
    
    df = df[df['database_0']==dataset][items]
    #df.replace(99,pd.NA,inplace=True)
    df.fillna('#/NA',inplace=True)
    return df
    

def calcule(preffix,df,dataset,var,items,n_items):
    
    print(f"Computer {dataset} {var} {preffix} {items} to {n_items}")

    o_items = [preffix+'_'+item+"_0" for item in items]
    f_items = [preffix+'_'+n_item+"_0" for n_item in n_items]

    df[f_items] = 0
    for indx,row in df.iterrows():
        
        for i_f,f_item in enumerate(f_items):
            oo_items = [ it for i,it in enumerate(o_items) if i % 4 == i_f]
            try:
                df.loc[indx,f_item]= row[oo_items].sum(numeric_only=True)
            except Exception as e:
                df.loc[indx,f_item] = "#/NA"

    r = o_items+f_items
    return df,r

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ["pdi1", "pdi1a", "pdi1b", "pdi1c", "pdi2", "pdi2a", "pdi2b", "pdi2c", "pdi3", "pdi3a", "pdi3b", "pdi3c", "pdi4", "pdi4a", "pdi4b", "pdi4c", "pdi5", "pdi5a", "pdi5b", "pdi5c", "pdi6", "pdi6a", "pdi6b", "pdi6c", "pdi7", "pdi7a", "pdi7b", "pdi7c", "pdi8", "pdi8a", "pdi8b", "pdi8c", "pdi9", "pdi9a", "pdi9b", "pdi9c", "pdi10", "pdi10a", "pdi10b", "pdi10c", "pdi11", "pdi11a", "pdi11b", "pdi11c", "pdi12", "pdi12a", "pdi12b", "pdi12c", "pdi13", "pdi13a", "pdi13b", "pdi13c", "pdi14", "pdi14a", "pdi14b", "pdi14c", "pdi15", "pdi15a", "pdi15b", "pdi15c", "pdi16", "pdi16a", "pdi16b", "pdi16c", "pdi17", "pdi17a", "pdi17b", "pdi17c", "pdi18", "pdi18a", "pdi18b", "pdi18c", "pdi19", "pdi19a", "pdi19b", "pdi19c", "pdi20", "pdi20a", "pdi20b", "pdi20c", "pdi21", "pdi21a", "pdi21b", "pdi21c"]
    n_items = ["pun_tot_pdi", "punt_ans_pdi", "punt_preo_pdi", "punt_conv_pdi"]
    
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

    print("================End of harmonization=====================")'''