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
        df = pd.concat([meta, feat_df], axis=1)
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
                    raise ValueError(f"Column name '{col}' does not contain enough numeric parts to form 'mz_rt' format.")
        
        df.rename(columns=new_columns, inplace=True)
        
        df.drop(columns=['row ID', 'row m/z', 'row retention time'], inplace=True)
        
        return df

    