class FilterBlanks:
    def __init__(self, isToFilter:bool,propBlankFeats:float,propSamples:float):
        self.isToFilter = isToFilter
        self.propBlankFeats = propBlankFeats
        self.propSamples = propSamples