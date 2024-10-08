import os

from api.src.model.FilterBlanks import FilterBlanks
from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.service.create_file_service import CreateFileService
from api.src.service.pcoa_from_file_service import PcoaFromFileService


class UploadEditedCsvController:

    def __init__(self,request,session,app,pcoaFromFileService:PcoaFromFileService):
            self.request = request
            self.session = session
            self.app = app        
            self.pcoaFromFileService = pcoaFromFileService

    def executeUploadEditedCsv(self):
        fullFilePath = self._createFile()
        fileId = self.session.get('fileId')
        filterBlanks = FilterBlanks(self.request.form['shared'],self.request.form['prop_blank_feats'],self.request.form['prop_samples'])

        dataProcessingConfig = DataProcessingConfig(self.request.form['metric'], self.request.form['scaling'], self.request.form['normalization'], None,filterBlanks)
        if fullFilePath is None:
            return "FileId not found in session", 400
        file_path = os.path.join(self.app.config['UPLOADED_PATH'], fileId)

        if not os.path.exists(file_path):
            return "File not found", 404    
        
        pcoa = None
        with open(file_path, 'rb') as file:
            pcoa = self.pcoaFromFileService.handleFile(file,fileId,dataProcessingConfig)
        return pcoa

    def _createFile(self):
        createFileService = CreateFileService(self.request.files.get('file'),self.session)
        return createFileService.createFile()