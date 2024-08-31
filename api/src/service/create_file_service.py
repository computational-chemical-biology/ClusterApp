import os
import uuid


class CreateFileService:
    def __init__(self,file,session):
        self.file = file
        self.session = session
        pass
    

    def createFile(self):
        self._executeFileCreation(self.file)
        return self._getFile()

    
    def _executeFileCreation(self,file):
        if not os.path.exists('/ClusterApp/api/static/downloads'):
                os.makedirs('/ClusterApp/api/static/downloads', exist_ok=True)    

        fileId = str(uuid.uuid4())
        self.session['fileId'] = fileId
        file.save(os.path.join('/ClusterApp/api/static/downloads', fileId))

    def _getFile(self):
        fileId = self.session.get('fileId')
        if fileId is None:
            return None
            
        return os.path.join('/ClusterApp/api/static/downloads', fileId)