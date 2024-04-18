import os

from flask import render_template

from api.PcoaFactory import PcoaFactory


class UploadFormController():

    def __init__(self,request,session,app,pcoaFromFileService):
        self.request = request
        self.session = session
        self.app = app
        self.pcoaFromFileService = pcoaFromFileService
        

    def executeUploadForm(self):
        """
            get the file saved in the session and create a pcoa plot from it 
            
            Returns: the graph.html template with the pcoa plot if successful
            400: if the file was not found in the session
        """
        fileId = self.session.get('fileId')
        if fileId is None:
            return render_template('error.html', error='FileId not found in session')
            
        file_path = os.path.join(self.app.config['UPLOADED_PATH'], fileId)
            
        if not os.path.exists(file_path):
            raise Exception('File not found')
        
        pcoa = None
        with open(file_path, 'rb') as file:
            pcoa = self.pcoaFromFileService._handleFile(file,fileId)

        return render_template('graph.html', pcoa=pcoa)
            

    def _handleFile(self,file,fileId):
        try:
            factory = PcoaFactory(session=self.session)
            factory.createPcoaFromFile(file,fileId)
            return f'downloads/{fileId}/index.html'   
        except Exception as e:
            raise e
