import pandas as pd

#Multiple lists to dataframe-- text_content,text_label,text_pred,image_path,image_label,image_pred are lists
final_df=pd.DataFrame({'text_content':text_content,'text_label':text_label,'text_pred':text_pred,'image_path':image_path,'image_label':image_labels,'image_pred':image_pred})
