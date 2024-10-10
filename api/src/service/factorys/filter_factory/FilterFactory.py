from api.src.model.FilterBlanks import FilterBlanks
from api.src.service.factorys.filter_factory.FilterByBlanks import FilterByBlanks

class FilterFactory:
    def __init__(self, filter: FilterBlanks):
        self.filter = filter

    def apply_filter(self, df):
                
        if self.filter.isToFilter == "true":
            return FilterByBlanks(df,self.filter).execute()
