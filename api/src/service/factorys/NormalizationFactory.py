class NormalizationFactory:
    
    def __init__(self,normType:str):
        self.normType = normType

    #the idea here is to be an factory with different objects to represent different types of normalization
    def normalize(self,df):

        if self.normType == 'PQN':
            medians = df.median(axis=1)
            normalized_df = df.div(medians, axis=0)
            normalized_df *= medians.median()
            return normalized_df
        
        elif self.normType == 'TIC':
            normalized_df = df.apply(lambda a: a/sum(a), axis=1)
            return normalized_df
        
        #in case of no normalization just return the original dataframe
        else:
            return df


    