from api.src.service.factorys.normalization.PqnNormalization import PqnNormalization


class NormalizationFactory:
    
    def __init__(self,normType:str):
        self.normType = normType

    def normalize(self,df):

        if self.normType == 'PQN':
            pqn = PqnNormalization(df)
            return pqn.normalize()
        
        elif self.normType == 'TIC':
            normalized_df = df.apply(lambda a: a/sum(a), axis=1)
            return normalized_df
        
        #in case of no normalization just return the original dataframe
        else:
            return df


    