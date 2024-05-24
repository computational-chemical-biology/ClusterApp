from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.utils.PcoaFactory import PcoaFactory


class PcoaFromFileService:

    def __init__(self,session):
        self.session = session

    def _handleFile(self,file,fileId,dataProcessingConfig:DataProcessingConfig):
        try:
            factory = PcoaFactory(session=self.session)
            factory.createPcoaFromFile(file,fileId,dataProcessingConfig)
            return f'downloads/{fileId}/index.html'   
        except Exception as e:
            raise e 