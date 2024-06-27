import os
import re
from flask import Request
from api.src.service.gnps import Proteosafe
import pandas as pd

class CsvFromGnpsController:


    def __init__(self, request: Request, session,app):
        self.request = request
        self.session = session
        self.app = app
    
    def get_csv_from_gnps(self):
        taskId = self.request.form.get('taskId')
        gnps = Proteosafe(taskId, 'FBMN')
        gnps.get_gnps()
        meta = gnps.meta
        feat = gnps.feat
        return self._createCsv(feat,meta)
    
    def _createCsv(self,feat,meta):
        df = self._mergeDf(feat,meta)
        directoryPath = os.path.join(os.getcwd(), 'api/static/downloads')
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath, exist_ok=True)
        path = directoryPath+'/'+self.request.form.get('taskId')+ '.csv'
        df.to_csv(path)
        return path
        
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