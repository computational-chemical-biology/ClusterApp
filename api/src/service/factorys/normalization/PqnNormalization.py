import numpy as np
import pandas as pd


class PqnNormalization:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def normalize(self, ref_norm = "median" ):

        if ref_norm == "median":
            ref_spec = self.data.median(axis=0)
        elif ref_norm == "mean":
            ref_spec = self.data.mean(axis=0)
            
        quotion = self.data.T.div(ref_spec.values, axis=0)
        factor = quotion.median(axis=1)
        normalizedDf = self.data.div(factor.values, axis=1)

        return normalizedDf