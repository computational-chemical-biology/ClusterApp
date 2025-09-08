import os
import uuid
from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.model.FilterBlanks import FilterBlanks
from api.src.model.dto.EmperorPlotDto import EmperorPlotDto
from api.src.service.create_file_from_gpns_service import CreateFileFromGnpsService
from api.src.service.factorys.filter_factory.FilterFactory import FilterFactory
from api.src.service.filter_blank_from_gpns_service import FilterBlankFromGnpsService
from api.src.service.gnps import Proteosafe
import pandas as pd
from api.src.service.reformat_table_service import ReformatTableService
from api.src.utils.utils import filterBlanks, qiime2PCoA


class PcoaFactory:
    def __init__(self,session):
        self.session = session

    def createPcoaFromGnps(self,dataProcessingConfig:DataProcessingConfig,createFileFromGnpsService:CreateFileFromGnpsService):
        taskid = uuid.uuid4()
        gnps_result = Proteosafe(dataProcessingConfig.taskId, dataProcessingConfig.workflow)
        gnps_result.get_gnps()
        directory_path = os.path.join(os.getcwd(), 'api/static/downloads', str(taskid))
        filterResult = FilterBlankFromGnpsService(dataProcessingConfig.filterBlanks,gnps_result,createFileFromGnpsService).filter()

        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)

        if filterResult['isFiltered']:
            metaFeatDto = ReformatTableService().reformatTable(filterResult['dataframe'])
            pcoa_obj = self._createPcoa(meta=metaFeatDto.meta, feat=metaFeatDto.feat,dataProcessingConfig=dataProcessingConfig,taskId=taskid)     
            self._saveAndCreatePcoaDirs(pcoa_obj,taskid)
            return EmperorPlotDto(f'downloads/{taskid}/index.html', description=filterResult['description'])
        
        pcoa_obj = self._createPcoa(meta=gnps_result.meta, feat=gnps_result.feat,dataProcessingConfig=dataProcessingConfig,taskId=taskid)     
        self._saveAndCreatePcoaDirs(pcoa_obj,taskid)
        return EmperorPlotDto(f'downloads/{taskid}/index.html', description=filterResult['description'])
    

    def createPcoaFromFile(self, file, taskId, dataProcessingConfig:DataProcessingConfig) -> EmperorPlotDto:
        dataframe = pd.read_csv(file)
        pathToRemove = os.path.join(os.getcwd(), 'api/static/downloads', str(taskId))
        if os.path.exists(pathToRemove):
           os.remove(pathToRemove)

        filterMap = filterBlanks(dataframe, dataProcessingConfig.filterBlanks)
        self._normalizeDataFrame(filterMap['dataframe'])
        pcoaObject = self._reformatTable(feat_table=filterMap['dataframe'], taskId=taskId,dataProcessingConfig=dataProcessingConfig)
        pcoa = self._saveAndCreatePcoaDirs(pcoaObject, taskId)
        return EmperorPlotDto(pcoa, description=filterMap['description'])
    
    def _normalizeDataFrame(self,dataframe):
        empty_rows = dataframe[dataframe.isnull().all(axis=1)].index
        if not empty_rows.empty:
            dataframe.drop(empty_rows, inplace=True)

        empty_cols = dataframe.columns[dataframe.isnull().all()]
        if not empty_cols.empty:
            dataframe.drop(empty_cols, axis=1, inplace=True)

    def _filterBlanks(self,dataframe,filterBlanks:FilterBlanks):
        filterMap = FilterFactory(filterBlanks).apply_filter(dataframe)   

        return filterMap          
    

    def _saveAndCreatePcoaDirs(self,pcoa_obj,taskid):
        directory_path = os.path.join(os.getcwd(), 'api/static/downloads', str(taskid))
        pcoa = os.path.join(directory_path, 'index.html')
        pcoa_file = os.path.join(directory_path, f'{taskid}.qzv')
        pcoa_obj.visualization.save(pcoa_file)
        self.session['pcoa_file'] = pcoa_file
        return pcoa 
    
    def _createPcoa(self,meta,feat,dataProcessingConfig:DataProcessingConfig,taskId):
        
        directory_path = os.path.join(os.getcwd(), 'api/static/downloads', str(taskId))
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True) 
        return qiime2PCoA(meta, feat,
                                out_dir=directory_path,
                                dataProcessingConfig=dataProcessingConfig)
    
    def _reformatTable(self,feat_table,taskId,dataProcessingConfig:DataProcessingConfig):
        """
        This Method Prepare The Meta And Feat Table To qiime2 and Return the pcoa object
        """
        metaFeatDto = ReformatTableService().reformatTable(feat_table)
        return self._createPcoa(meta=metaFeatDto.meta,feat=metaFeatDto.feat,dataProcessingConfig=dataProcessingConfig,taskId=taskId)
    