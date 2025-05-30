import re
import pandas as pd


class CreateFileFromGnpsService:

    def __init__(self):
        pass

    def createFile(self,feat,meta):
        df = self._mergeDf(feat,meta)
        return df
        
    def _mergeDf(self,feat,meta):
        df = self.merge_dataframes_dynamic(meta,feat)
        return df

    
    def merge_dataframes_dynamic(self,meta,feat):
        feat2 = feat[feat.columns[feat.columns.str.contains('Peak area')]].T

        feat2.columns = feat.apply(lambda a: '{0}_{1}'.format(round(a['row m/z']), round(a['row retention time']*60)), axis=1).tolist()
        feat2 = feat2.reset_index()
        feat2['index'] = feat2['index'].str.replace(' Peak area', '')
        
        return pd.merge(meta, feat2, left_on='filename', right_on='index').drop(['index'], axis=1)
