import os

from flask import  redirect, url_for

from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.service.pcoa_from_file_service import PcoaFromFileService
from api.src.utils.utils import createFile, getFile


class UploadEditedCsvController:

    def __init__(self,request,session,app,pcoaFromFileService:PcoaFromFileService):
            self.request = request
            self.session = session
            self.app = app        
            self.pcoaFromFileService = pcoaFromFileService


    def executeUploadEditedCsv(self):
        createFile(self.request,self.session,self.app)
        fullFilePath = getFile(self.session,self.app)
        fileId = self.session.get('fileId')
        dataProcessingConfig = DataProcessingConfig(self.request.form['metric'], self.request.form['scaling'], self.request.form['normalization'], None)
        if fullFilePath is None:
            return "FileId not found in session", 400
            
        file_path = os.path.join(self.app.config['UPLOADED_PATH'], fullFilePath)

        if not os.path.exists(file_path):
            return "File not found", 404    
        
        with open(file_path, 'rb') as file:
            pcoa = self.pcoaFromFileService._handleFile(file,fileId,dataProcessingConfig)
        return redirect(url_for('render_graph', pcoa=pcoa))
