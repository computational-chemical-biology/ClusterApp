from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.service.pcoa_from_file_service import PcoaFromFileService
from api.src.model.FilterBlanks import FilterBlanks
import uuid

class DropzoneUploadHandler:
    
    def __init__(self,request,session,app,pcoaFromFileService:PcoaFromFileService):
        self.request = request
        self.session = session
        self.app = app
        self.pcoaFromFileService = pcoaFromFileService


    def executeDropzoneUpload(self):
        file = self.request.files['file']
        scalling = self.request.form['scaling'] 
        normalization = self.request.form['normalization']
        filterBlanks = FilterBlanks(self.request.form['filter_blanks_ch_dz'],self.request.form['prop_blank_feats'],self.request.form['prop_samples'])
        dataProcessingConfig = DataProcessingConfig(self.request.form['metric'], scalling, normalization, filterBlanks)

        fileId = uuid.uuid4()
        self.session['fileId'] = fileId
        
        return self.pcoaFromFileService.handleFile(file, fileId, dataProcessingConfig)