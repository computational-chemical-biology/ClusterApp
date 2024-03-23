import os
import uuid
from api.gnps import Proteosafe
from api.utils import makePcoa, qiime2PCoA
import pandas as pd


class PcoaFactory:
    def __init__(self,session):
        self.session = session
        pass

    def getPcoaFromGnps(self,request):
        taskid = uuid.uuid4()
        gnps_result = Proteosafe(request.form['taskid'], 'FBMN')
        gnps_result.get_gnps()
        directory_path = os.path.join(os.getcwd(), 'api/static/downloads', str(taskid))
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
        pcoa_obj = self._createPcoa(meta=gnps_result.meta, feat=gnps_result.feat,metric=request.form['metric'],taskId=taskid)     
        pcoa = self._saveAndCreatePcoaDirs(pcoa_obj,taskid)
        return pcoa
    

    def getPcoaFromFile(self,file):
        dataframe = pd.read_csv(file)
        taskid = uuid.uuid4()
        pcoaObject = self._reformatTable(dataframe,taskid)
        pcoa = self._saveAndCreatePcoaDirs(pcoaObject,taskid)
        return pcoa
    
    

    def _saveAndCreatePcoaDirs(self,pcoa_obj,taskid):
        directory_path = os.path.join(os.getcwd(), 'api/static/downloads', str(taskid))
        pcoa = os.path.join(directory_path, 'index.html')
        pcoa_file = os.path.join(directory_path, f'{taskid}.qzv')
        pcoa_obj.visualization.save(pcoa_file)
        self.session['pcoa_file'] = pcoa_file
        return pcoa 
    
    def _createPcoa(self,meta,feat,metric,taskId):
        
        directory_path = os.path.join(os.getcwd(), 'api/static/downloads', str(taskId))
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True) 
        return qiime2PCoA(meta, feat,
                                out_dir=directory_path,
                                metric=metric)
    
    def _reformatTable(self,feat_table,taskId):
        """
        This Method Prepare The Meta And Feat Table To qiime2 and Return the pcoa object
            
        """
        last_attr = feat_table.columns[feat_table.columns.str.contains('ATTRIBUTE')][-1]
        plast_attr = feat_table.columns.get_loc(last_attr)+1
        meta = feat_table[feat_table.columns[:plast_attr]]
        meta.filename+' Peak area'
        feat = feat_table[feat_table.columns[plast_attr:]].T
        feat.columns = meta.filename+' Peak area'
        feat_tmp = pd.DataFrame(feat.index)
        feat_tmp.reset_index(inplace=True)
        feat_tmp = pd.DataFrame(feat_tmp[0].apply(lambda a: a.split("_")).tolist())
        feat_tmp.reset_index(inplace=True)

        feat_tmp.columns = ['row ID', 'row m/z', 'row retention time']
        feat = pd.concat([feat_tmp, feat.reset_index(drop=True)], axis=1)
        return self._createPcoa(meta=meta,feat=feat,metric='euclidean',taskId=taskId)
    
    
    


   