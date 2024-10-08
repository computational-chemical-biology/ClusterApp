import unittest
import pandas as pd
import numpy as np

from api.src.service.factorys.ScalingFactory import ScalingFactory

class TestScalingFactory(unittest.TestCase):

    def test_scaling_factory_pareto(self):
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
        factory = ScalingFactory(scaling='pareto')
        scaled_df = factory.scale(df)

        expected_df = (df - df.mean()) / np.sqrt(df.std())
        pd.testing.assert_frame_equal(scaled_df, expected_df)

    def test_scaling_factory_autoscaling(self):
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
        factory = ScalingFactory(scaling='autoscaling')
        scaled_df = factory.scale(df)

        expected_df = (df - df.mean()) / df.std()
        pd.testing.assert_frame_equal(scaled_df, expected_df)

    def test_scaling_factory_no_scaling(self):
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
        factory = ScalingFactory(scaling='none')
        scaled_df = factory.scale(df)

        pd.testing.assert_frame_equal(scaled_df, df)

    def test_scaling_factory_invalid_scaling(self):
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        
        factory = ScalingFactory(scaling='invalid_scaling')
        scaled_df = factory.scale(df)

        pd.testing.assert_frame_equal(scaled_df, df)

if __name__ == '__main__':
    unittest.main()
