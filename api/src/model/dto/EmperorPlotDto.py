class EmperorPlotDto():

    def __init__(self, emperorDir = '',description = ''):
        self.emperorDir = emperorDir
        self.description = description

    def serialize(self):
        return {
            'emperorDir': self.emperorDir,
            'description': self.description
        }