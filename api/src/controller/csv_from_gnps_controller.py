import os
from flask import Request
from api.src.service.create_file_from_gpns_service import CreateFileFromGnpsService
from api.src.service.gnps import Proteosafe

class CsvFromGnpsController:


    def __init__(self, request: Request, session,app,createFileFromGnpsService:CreateFileFromGnpsService):
        self.request = request
        self.session = session
        self.app = app
        self.createFileFromGnpsService = createFileFromGnpsService
    
    def get_csv_from_gnps(self):
        taskId = self.request.form.get('taskId')
        workflow = self.request.form.get('workflow')
        gnps = Proteosafe(taskId, workflow)
        gnps.get_gnps()
        meta = gnps.meta
        feat = gnps.feat
        return self._createCsv(feat,meta)
    
    
    
    def _createCsv(self,feat,meta):
        df = self.createFileFromGnpsService.createFile(feat,meta)
        directoryPath = os.path.join(os.getcwd(), 'api/static/downloads')
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath, exist_ok=True)
        path = directoryPath+'/'+self.request.form.get('taskId')+ '.csv'
        df.to_csv(path,index=False)
        return path