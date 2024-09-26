import unittest
from unittest.mock import MagicMock, patch
import os
import uuid
from api.src.service.create_file_service import CreateFileService 

class TestCreateFileService(unittest.TestCase):

    @patch('api.src.service.create_file_service.os.makedirs')
    @patch('api.src.service.create_file_service.os.path.exists')
    def test_executeFileCreation_creates_directory_and_saves_file(self, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        session = {}
        file = MagicMock()
        service = CreateFileService(file, session)
        
        service._executeFileCreation(file)
        
        mock_makedirs.assert_called_once_with('/ClusterApp/api/static/downloads', exist_ok=True)
        
        fileId = session['fileId']
        file.save.assert_called_once_with(os.path.join('/ClusterApp/api/static/downloads', fileId))

    def test_getFile_returns_file_path(self):
        session = {'fileId': 'some-uuid'}
        service = CreateFileService(None, session)
        
        file_path = service._getFile()
        
        expected_path = os.path.join('/ClusterApp/api/static/downloads', 'some-uuid')
        self.assertEqual(file_path, expected_path)

    def test_getFile_returns_None_when_fileId_is_missing(self):
        session = {}
        service = CreateFileService(None, session)
        
        file_path = service._getFile()
        
        self.assertIsNone(file_path)

    @patch.object(CreateFileService, '_executeFileCreation')
    @patch.object(CreateFileService, '_getFile')
    def test_createFile_calls_internal_methods(self, mock_getFile, mock_executeFileCreation):
        file = MagicMock()
        session = {}
        service = CreateFileService(file, session)
        
        service.createFile()
        
        mock_executeFileCreation.assert_called_once_with(file)
        mock_getFile.assert_called_once()

if __name__ == '__main__':
    unittest.main()
