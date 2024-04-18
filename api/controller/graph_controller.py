from flask import render_template
from api.PcoaFactory import PcoaFactory


class GraphController:

    def __init__(self,request,session):
        self.request = request
        self.session = session

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
        factory = PcoaFactory(session=self.session)
        taskId =  factory.createPcoaFromGnps(request=self.request)
        return f'downloads/{taskId}/index.html'