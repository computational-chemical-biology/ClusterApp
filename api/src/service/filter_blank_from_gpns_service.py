from api.src.model.FilterBlanks import FilterBlanks
from api.src.service.create_file_from_gpns_service import CreateFileFromGnpsService
from api.src.service.factorys.filter_factory.FilterFactory import FilterFactory


class FilterBlankFromGnpsService:
    
    def __init__(self,filterBlanks:FilterBlanks,gnpsResult,createFileFromGnpsService:CreateFileFromGnpsService):
        self.filterBlanks = filterBlanks
        self.gnpsResult = gnpsResult
        self.createFileFromGnpsService = createFileFromGnpsService

    def filter(self):
        if not self.filterBlanks.isToFilter:
            return {'dataframe':None, 'description': None,'isFiltered':False} 
        return self._executeFilter()

    def _executeFilter(self):
        df = self.createFileFromGnpsService.createFile(self.gnpsResult.feat.copy(),self.gnpsResult.meta.copy())
        filterFactory = FilterFactory(self.filterBlanks)
        return filterFactory.apply_filter(df)
