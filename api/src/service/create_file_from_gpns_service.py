import re
import pandas as pd


class CreateFileFromGnpsService:

    def __init__(self):
        pass

    def createFile(self,feat,meta):
        df = self._mergeDf(feat,meta)
        return df
        
    def _mergeDf(self,feat,meta):
        feat_df = self._rename_columns(feat)
        df = self.merge_dataframes_dynamic(meta,feat_df)
        return df

    def _rename_columns(self,df):
        new_columns = {}
        for col in df.columns:
            if col.strip() == '' or col.startswith('Unnamed:'):
                df.drop(columns=[col], inplace=True)
            elif col not in ['row ID', 'row m/z', 'row retention time']:
                matches = re.findall(r'(\d+)', col)
                if len(matches) >= 2:
                    mz = matches[0]
                    rt = matches[1]
                    new_col_name = f"{mz}_{rt}"
                    new_columns[col] = new_col_name
                else:
                    df.drop(columns=[col], inplace=True)
        
        df.rename(columns=new_columns, inplace=True)
        
        df.drop(columns=['row ID', 'row m/z', 'row retention time'], inplace=True)
        
        return df
    
    def merge_dataframes_dynamic(self,df1, df2):

        n_rows = min(len(df1), len(df2))
        
        df1_trimmed = df1.iloc[:n_rows].reset_index(drop=True)
        df2_trimmed = df2.iloc[:n_rows].reset_index(drop=True)
        
        merged_df = pd.concat([df1_trimmed, df2_trimmed], axis=1)
        
        return merged_df

    