from api.src.utils.PcoaFactory import PcoaFactory


class PcoaFromFileService:

    def __init__(self,session):
        self.session = session

    def _handleFile(self,file,fileId):
        try:
            factory = PcoaFactory(session=self.session)
            factory.createPcoaFromFile(file,fileId)
            return f'downloads/{fileId}/index.html'   
        except Exception as e:
            raise e 