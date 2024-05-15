import numpy as np


class ScalingFactory:
    def __init__(self, scaling):
        self.scaling = scaling

    # the idea here is to be an factory with different objects to represent different types of scaling
    def scale(self, df):
        if self.scaling == 'pareto':
            scaled_df = (df - df.mean()) / np.sqrt(df.std())
            return scaled_df
        
        return (df-df.mean())/df.std()