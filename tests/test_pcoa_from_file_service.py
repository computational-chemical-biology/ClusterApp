import unittest
from unittest.mock import MagicMock, patch

from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.service.pcoa_from_file_service import PcoaFromFileService


class TestPcoaFromFileService(unittest.TestCase):

    
    @patch('api.src.service.pcoa_from_file_service.PcoaFactory')
    def test_handle_file_returns_valid_path(self, MockPcoaFactory):
        session = {}
        file = MagicMock()
        file_id = 'fileId'
        data_processing_config = MagicMock(spec=DataProcessingConfig)

        mock_pcoa_factory = MockPcoaFactory.return_value
        mock_pcoa_factory.createPcoaFromFile.return_value = None  

        pcoa_service = PcoaFromFileService(session)
        
        result = pcoa_service.handleFile(file, file_id, data_processing_config)

        MockPcoaFactory.assert_called_once_with(session=session)

        mock_pcoa_factory.createPcoaFromFile.assert_called_once_with(file, file_id, data_processing_config)

        expected_path = f'downloads/{file_id}/index.html'
        self.assertEqual(result, expected_path)

if __name__ == '__main__':
    unittest.main()
