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
        generateRepportChDz = self.request.form['generate_repport_ch_dz'] == 'true'
        fileId = uuid.uuid4()
        if generateRepportChDz:
            return self.pcoaFromFileService.handleGenerateReport(file,fileId)

        dataProcessingConfig = DataProcessingConfig(metric=self.request.form['metric'],scaling= scalling, normalization= normalization,taskId= None,filterBlanks= filterBlanks)

        self.session['fileId'] = fileId
        
        return self.pcoaFromFileService.handleFile(file, fileId, dataProcessingConfig)