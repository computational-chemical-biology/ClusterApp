import unittest
from unittest.mock import Mock, patch
import pandas as pd

from api.src.service.factorys.normalization.NormalizationFactory import NormalizationFactory

class TestNormalizationFactory(unittest.TestCase):

    @patch('api.src.service.factorys.normalization.PqnNormalization')
    def test_normalization_factory_pqn(self, MockPqnNormalization):
        MockPqnNormalization.normalize.return_value = pd.DataFrame({
            'A': [1.0, 2.0, 3.0],
            'B': [4.0,5.0, 6.0]
        })

        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        factory = NormalizationFactory(normType='PQN')
        normalized_df = factory.normalize(df)

        self.assertTrue(normalized_df.equals(MockPqnNormalization.normalize.return_value))

    def test_normalization_factory_tic(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        factory = NormalizationFactory(normType='TIC')
        normalized_df = factory.normalize(df)

        expected_df = df.apply(lambda a: a / sum(a), axis=1)
        self.assertTrue(normalized_df.equals(expected_df))

    def test_normalization_factory_no_normalization(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        factory = NormalizationFactory(normType='NONE')
        normalized_df = factory.normalize(df)

        self.assertTrue(normalized_df.equals(df))

if __name__ == '__main__':
    unittest.main()
