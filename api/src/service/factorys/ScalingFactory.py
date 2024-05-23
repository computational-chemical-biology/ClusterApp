import numpy as np


class ScalingFactory:
    def __init__(self, scaling:str):
        self.scaling = scaling

    # the idea here is to be an factory with different objects to represent different types of scaling
    def scale(self, df):
        if self.scaling == 'pareto':
            scaled_df = (df - df.mean()) / np.sqrt(df.std())
            return scaled_df

        elif self.scaling == 'autoscaling':
            scaled_df = (df - df.mean()) / (df.std())
            return scaled_df
        
        #in case of no scaling just return the original dataframe
        else:
            return df
