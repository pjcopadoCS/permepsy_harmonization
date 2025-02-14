import os
import pandas as pd

def harmonize(df,dataset,var):

    items ='''pre_CBQ_1, pre_CBQ_2, pre_CBQ_3, pre_CBQ_4, pre_CBQ_5, pre_CBQ_6, pre_CBQ_7,pre_CBQ_8, pre_CBQ_9,pre_CBQ_10, pre_CBQ_11,pre_CBQ_12,
    pre_CBQ_13,pre_CBQ_14, pre_CBQ_15, pre_CBQ_16,pre_CBQ_17, pre_CBQ_18, pre_CBQ_19, pre_CBQ_20, pre_CBQ_21, pre_CBQ_22, pre_CBQ_23, pre_CBQ_24,
    pre_CBQ_25,pre_CBQ_26, pre_CBQ_27, pre_CBQ_28, pre_CBQ_29, pre_CBQ_30, post_CBQ_1, post_CBQ_2, post_CBQ_3, post_CBQ_4, post_CBQ_5, post_CBQ_6,
    post_CBQ_7, post_CBQ_8, post_CBQ_9, post_CBQ_10, post_CBQ_11, post_CBQ_12, post_CBQ_13, post_CBQ_14, post_CBQ_15, post_CBQ_16, post_CBQ_17,
    post_CBQ_18, post_CBQ_19, post_CBQ_20, post_CBQ_21, post_CBQ_22, post_CBQ_23,post_CBQ_24, post_CBQ_25, post_CBQ_26, post_CBQ_27, post_CBQ_28, 
    post_CBQ_29, post_CBQ_30'''

    new_items = '''pre_CBQ_I, pre_CBQ_C, pre_CBQ_DT, pre_CBQ_JTC, pre_CBQ_ER, pre_CBQ_T,post_CBQ_I, post_CBQ_C, post_CBQ_DT, post_CBQ_JTC, 
    post_CBQ_ER, post_CBQ_T'''

    items = [item.strip()+"_0" for item in items.replace("\n","").split(",")]
    new_items = [item.strip()+"_0" for item in new_items.replace("\n","").split(",")]

    I = [1,3,20,22,23,28]
    C = [2,4,7,10,12,25]
    DT = [5,11,14,15,27,30]
    JTC = [6,9,17,18,21,29]
    ER = [8,13,16,19,29,26]
    
    print(f"Harmonizing {var}...on {dataset}")
    
    for indx,it in enumerate(new_items):
        if it not in df.columns:
            if 'pre_' in it:
                df.insert(df.columns.get_loc('pre_CBQ_30_0')+indx,it,0)
            else:
                df.insert(df.columns.get_loc('post_CBQ_30_0')+indx,it,0)
    
    dfp = df[df['database_0']==dataset][items]
    
    dfp.to_csv('output'+os.sep+"before_"+dataset+'_'+var+'.csv',index=False)
    
    dfp['pre_CBQ_I_0'] = 0
    dfp['post_CBQ_I_0'] = 0
    for i in I:
        dfp['pre_CBQ_I_0'] += dfp['pre_CBQ_'+str(i)+"_0"]
        dfp['post_CBQ_I_0'] += dfp['post_CBQ_'+str(i)+"_0"]
    
    dfp['pre_CBQ_C_0'] = 0
    dfp['post_CBQ_C_0'] = 0
    for i in C:
        dfp['pre_CBQ_C'+"_0"] += dfp['pre_CBQ_'+str(i)+"_0"]
        dfp['post_CBQ_C'+"_0"] += dfp['post_CBQ_'+str(i)+"_0"]
        
    dfp['pre_CBQ_DT'+"_0"] = 0
    dfp['post_CBQ_DT'+"_0"] = 0
    for i in DT:
        dfp['pre_CBQ_DT'+"_0"] += dfp['pre_CBQ_'+str(i)+"_0"]
        dfp['post_CBQ_DT'+"_0"] += dfp['post_CBQ_'+str(i)+"_0"]
    
    dfp['pre_CBQ_JTC'+"_0"] = 0
    dfp['post_CBQ_JTC'+"_0"] = 0
    for i in JTC:
        dfp['pre_CBQ_JTC'+"_0"] += dfp['pre_CBQ_'+str(i)+"_0"]
        dfp['post_CBQ_JTC'+"_0"] += dfp['post_CBQ_'+str(i)+"_0"]
        
    dfp['pre_CBQ_ER'+"_0"] = 0
    dfp['post_CBQ_ER'+"_0"] = 0
    for i in ER:
        dfp['pre_CBQ_ER'+"_0"] += df['pre_CBQ_'+str(i)+"_0"]
        dfp['post_CBQ_ER'+"_0"] += df['post_CBQ_'+str(i)+"_0"]    
    
    dfp['pre_CBQ_T'+"_0"] = dfp['pre_CBQ_I'+"_0"]+dfp['pre_CBQ_C'+"_0"]+dfp['pre_CBQ_DT'+"_0"]+dfp['pre_CBQ_JTC'+"_0"]+dfp['pre_CBQ_ER'+"_0"]
    dfp['post_CBQ_T'+"_0"] = dfp['post_CBQ_I'+"_0"]+dfp['post_CBQ_C'+"_0"]+dfp['post_CBQ_DT'+"_0"]+dfp['post_CBQ_JTC'+"_0"]+dfp['post_CBQ_ER'+"_0"]
    
    pre_items = [w for w in items+new_items if 'pre' in w]
    post_items = [w for w in items+new_items if 'post' in w]
    
    dfp[pre_items+post_items].to_csv('output'+os.sep+"after_"+dataset+'_'+var+'.csv',index=False)
    df.loc[df['database_0']==dataset,pre_items+post_items] = dfp.values
    
    items = pre_items + post_items
    for it in items:
        df[dataset][it] = dfp[it].values  
    
    df.to_csv('output'+os.sep+"after_all_"+dataset+'_'+var+'.csv',index=False)