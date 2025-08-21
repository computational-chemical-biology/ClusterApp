from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.model.dto.EmperorPlotDto import EmperorPlotDto
from api.src.service.create_plots_service import CreatePlotsService
from api.src.service.generate_repport_service import GenerateRepportService
from api.src.service.reformat_table_service import ReformatTableService
from api.src.utils.PcoaFactory import PcoaFactory
import pandas as pd


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

    def handleGenerateReport(self,file,uuid:str):
        try:
            dataframe = pd.read_csv(file)
            dataframe['filename'] = dataframe['filename']+'.mzML'
            metaFeatDto = ReformatTableService().reformatTable(dataframe)
            plots = CreatePlotsService(metaFeatDto=metaFeatDto,uuid=uuid).create()
            path = GenerateRepportService(plots).generate_repport(output_path=f'{uuid}.pdf')
            return path
        except Exception as e:
            raise e