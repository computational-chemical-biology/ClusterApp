from flask import render_template
from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.utils.PcoaFactory import PcoaFactory

class GraphController:

    def __init__(self,request,session,app):
        self.request = request
        self.session = session
        self.app = app

    def executeGraph(self):
        """
        create a pcoa plot from data provided by the gnps with taskid of the user input
        Returns:
            the graph.html template with the pcoa plot if POST request
            graph.html if GET request 
        """  
        pcoa = None
        if self.request.method == 'POST':
            pcoa = self.executePost()
        
        return render_template('graph.html', pcoa=pcoa)
    

    def executePost(self):
        scalling = self.request.form['scaling']  if self.request.form['scaling'] != None else None
        normalization = self.request.form['normalization'] if self.request.form['normalization'] != None else None
        dataProcessingConfig = DataProcessingConfig(self.request.form['metric'], scalling, normalization, self.request.form['taskid'])

        factory = PcoaFactory(session=self.session)
        taskId =  factory.createPcoaFromGnps(dataProcessingConfig=dataProcessingConfig)
        return f'downloads/{taskId}/index.html'


