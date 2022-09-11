import pandas as pd

#Multiple lists to dataframe-- text_content,text_label,text_pred,image_path,image_label,image_pred are lists
final_df=pd.DataFrame({'text_content':text_content,'text_label':text_label,'text_pred':text_pred,'image_path':image_path,'image_label':image_labels,'image_pred':image_pred})

#create new column based on condition of two other columns
def new_fn(df):
    if df.column1=="abc" or df.column2=="xyz":
        return "yes"
    else:
        return "no"
df['new_column'] = df.apply(new_fn, axis=1)
