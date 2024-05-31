from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.service.pcoa_from_file_service import PcoaFromFileService
import uuid

class DropzoneUploadHanlder:
    
    def __init__(self,request,session,app,pcoaFromFileService:PcoaFromFileService):
        self.request = request
        self.session = session
        self.app = app
        self.pcoaFromFileService = pcoaFromFileService


    def executeDropzoneUpload(self):
        file = self.request.files['file']
        scalling = self.request.form['scaling']  if self.request.form['scaling'] != None else None
        normalization = self.request.form['normalization'] if self.request.form['normalization'] != None else None
        dataProcessingConfig = DataProcessingConfig(self.request.form['metric'], scalling, normalization, None)

        fileId = uuid.uuid4()
        self.session['fileId'] = fileId
        
        return self.pcoaFromFileService.handleFile(file, fileId, dataProcessingConfig)

