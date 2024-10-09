from api.src.model.FilterBlanks import FilterBlanks
from api.src.service.factorys.filter_factory.FilterByBlankInFilename import FilterByBlankInFilename
from api.src.service.factorys.filter_factory.FilterByBlanks import FilterByBlanks

class FilterFactory:
    def __init__(self, filter: FilterBlanks):
        self.filter = filter

    def apply_filter(self, df):
                
        if self.filter.filterByName == "true":
            return FilterByBlankInFilename(df).execute()
        if self.filter.filterByName == "false":
            return FilterByBlanks(df,self.filter).execute()
