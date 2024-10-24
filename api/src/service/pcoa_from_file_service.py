from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.model.dto.EmperorPlotDto import EmperorPlotDto
from api.src.utils.PcoaFactory import PcoaFactory


class PcoaFromFileService:

    def __init__(self,session):
        self.session = session

    def handleFile(self,file,fileId,dataProcessingConfig:DataProcessingConfig) -> EmperorPlotDto:
        try:
            factory = PcoaFactory(session=self.session)
            emperorPlotDto = factory.createPcoaFromFile(file,fileId,dataProcessingConfig)
            emperorPlotDto.emperorDir = f'downloads/{fileId}/index.html'   
            return emperorPlotDto
        except Exception as e:
            raise e 