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
    
    def merge_dataframes_dynamic(self,meta,feat):

        feat.apply(lambda a: '{0}_{1}'.format(round(a['row m/z']), round(a['row retention time']*60)), axis=1)        
        feat2 = feat[feat.columns[feat.columns.str.contains('Peak area')]].T
        feat2.columns = feat.apply(lambda a: '{0}_{1}'.format(round(a['row m/z']), round(a['row retention time']*60)), axis=1).tolist()
        feat2 = feat2.reset_index()
        feat2['index'] = feat2['index'].str.replace(' Peak area', '')
        
        return pd.merge(meta, feat2, left_on='filename', right_on='index').drop(['index'], axis=1).to_csv('example_file_clusterapp.csv', index=None)

    