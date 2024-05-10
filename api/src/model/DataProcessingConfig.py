class DataProcessingConfig:

    def __init__(self, metric:str, scaling:str, normalization:str, taskId:str):
        self.metric = metric
        self.scaling = scaling
        self.normalization = normalization
        self.taskId = taskId
