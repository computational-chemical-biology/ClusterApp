import os
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
        df = pd.concat([meta,feat], axis=1, join="inner")
        df.fillna('empty', inplace=True)
        return df 
