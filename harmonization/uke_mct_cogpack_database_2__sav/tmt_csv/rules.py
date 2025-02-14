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

	for indx,row in df.iterrows():
		
		for i in range(len(n_items)):
			
			o_item = preffix+'_'+items[i]+"_0"
			f_item = preffix+'_'+n_items[i]+"_0"
		
			try:
				df.loc[indx,f_item]= float(row[o_item])
			except Exception as e:
				df.loc[indx,f_item] = pd.NA
	print("Done")
	r = [preffix+'_'+i+'_0' for i in n_items]
	return df,r

def harmonize(df,dataset,var):
    
    print(f"Harmonizing {var}...on {dataset}")
    items = ["TMT_A_pd","TMT_B_pd"]
    n_items = ["TMT_A_pd","TMT_B_pd"]
    
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