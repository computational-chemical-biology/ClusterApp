import os

from flask import  redirect, render_template, url_for
from api import app
from api.PcoaFactory import PcoaFactory
from api.utils import createFile, getFile


class UploadEditedCsvController:

    def __init__(self,request,session,app):
            self.request = request
            self.session = session
            self.app = app        


    def executeUploadEditedCsv(self):
        createFile(self.request,self.session,self.app)
        fullFilePath = getFile(self.session,self.app)
        fileId = self.session.get('fileId')

        if fullFilePath is None:
            return "FileId not found in session", 400
            
        file_path = os.path.join(self.app.config['UPLOADED_PATH'], fullFilePath)

        if not os.path.exists(file_path):
            return "File not found", 404    
        
        with open(file_path, 'rb') as file:
            pcoa = self._handleFile(file,fileId)
        return redirect(url_for('render_graph', pcoa=pcoa))


    def _handleFile(self,file,fileId):
        try:
            factory = PcoaFactory(session=self.session)
            factory.createPcoaFromFile(file,fileId)
            return f'downloads/{fileId}/index.html'   
        except Exception as e:
            raise e 
