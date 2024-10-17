from flask import jsonify, render_template
from api.src.model.FilterBlanks import FilterBlanks
from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.service.create_file_from_gpns_service import CreateFileFromGnpsService
from api.src.utils.PcoaFactory import PcoaFactory

class GraphController:

    def __init__(self,request,session,app,createFileFromGnpsService:CreateFileFromGnpsService):
        self.request = request
        self.session = session
        self.app = app
        self.createFileFromGnpsService = createFileFromGnpsService

    def executeGraph(self):
        """
        create a pcoa plot from data provided by the gnps with taskid of the user input
        Returns:
            the graph.html template with the pcoa plot if POST request
            graph.html if GET request 
        """  
        if self.request.method == 'POST':
            return jsonify({'emperor_plot':self.executePost().serialize()})
        
        return render_template('graph.html')
    

    def executePost(self):
        scalling = self.request.form['scaling'] 
        normalization = self.request.form['normalization'] 
        filterBlanks = self._createFilterBlanks()
        dataProcessingConfig = DataProcessingConfig(self.request.form['metric'], scalling, normalization, self.request.form['taskid'],self.request.form['workflow'],filterBlanks)
        factory = PcoaFactory(session=self.session)
        emperorPlot =  factory.createPcoaFromGnps(dataProcessingConfig=dataProcessingConfig,createFileFromGnpsService=self.createFileFromGnpsService)
        return emperorPlot

    def _createFilterBlanks(self):
        shared = True if self.request.form.get('shared', None) == 'on' else False
        prop_blank_feats = self.request.form.get('prop_blank_feats',None)
        prop_samples = self.request.form.get('prop_samples',None)

        return FilterBlanks(shared, prop_blank_feats, prop_samples)
        
