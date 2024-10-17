
import pandas as pd

from api.src.model.dto.MetaFeatDto import MetaFeatDto


class ReformatTableService:

    def __init__(self):
        pass
         
    
    def reformatTable(self,feat_table):
        last_attr = feat_table.columns[feat_table.columns.str.contains('ATTRIBUTE')][-1]
        plast_attr = feat_table.columns.get_loc(last_attr)+1
        meta = feat_table[feat_table.columns[:plast_attr]]
        meta.columns = meta.columns.str.replace('Filename', 'filename')
        meta.filename+' Peak area'
        meta.fillna('empty', inplace=True)
        meta = meta.astype(str)
        feat = feat_table[feat_table.columns[plast_attr:]].T
        feat.columns = meta.filename+' Peak area'
        feat_tmp = pd.DataFrame(feat.index)
        feat_tmp.reset_index(inplace=True)
        feat_tmp = pd.DataFrame(feat_tmp[0].apply(lambda a: a.split("_")[:2]).tolist())
        feat_tmp.reset_index(inplace=True)
        
        feat_tmp.columns = ['row ID', 'row m/z', 'row retention time']
        feat = pd.concat([feat_tmp, feat.reset_index(drop=True)], axis=1)
        return MetaFeatDto(feat=feat,meta=meta)