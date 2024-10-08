from api.src.model.FilterBlanks import FilterBlanks

class DataProcessingConfig:

    def __init__(self, metric:str, scaling:str, normalization:str, taskId:str,workflow:str = 'FBMN',filterBlanks:FilterBlanks = None):
        self.metric = metric
        self.scaling = scaling
        self.normalization = normalization
        self.taskId = taskId
        self.workflow = workflow
        self.filterBlanks = filterBlanks
