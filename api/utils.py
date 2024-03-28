import os
import re
import pandas as pd
import numpy as np
import qiime2
from qiime2 import Artifact
from qiime2.plugins import metadata, feature_table, diversity, emperor
from q2_emperor import plot, procrustes_plot, biplot, generic_plot
from scipy.spatial.distance import squareform, pdist
import skbio
import uuid


def qiime2PCoA(sample_metadata, df, out_dir, norm=True,
                              scale=False, metric='canberra'):
    sample_metadata.rename(index=str, columns={"filename": "#SampleID"},
                           inplace=True)
    sample_metadata.columns = sample_metadata.columns.str.replace('\s', '_')

    sample_metadata.index = sample_metadata['#SampleID']
    sample_metadata.drop(['#SampleID'], axis=1, inplace=True)
    qsample_metadata = qiime2.metadata.Metadata(sample_metadata)

    df2 = df[df.columns[df.columns.str.contains(' Peak area')]]
    df2.columns = [re.sub('(.+\.mzX?ML) .+', '\\1', a) for a in df2.columns]
    df2.index = df['row ID'].astype(str)
    df2 = df2.T

    if norm:
        df2 = df2.apply(lambda a: a/sum(a), axis=1)

    if scale:
        df2 = (df2-df2.mean())/df2.std()

    dm1 = squareform(pdist(df2, metric=metric))
    dm1 = skbio.DistanceMatrix(dm1, ids=df2.index.tolist())
    dm1 = Artifact.import_data("DistanceMatrix", dm1)
    pcoa = diversity.methods.pcoa(dm1)
    emperor_plot = emperor.visualizers.plot(pcoa.pcoa, qsample_metadata)

    if '.qzv' in out_dir:
        emperor_plot.visualization.save(out_dir)
    else:
        emperor_plot.visualization.export_data(out_dir)
    return emperor_plot

def makePcoa(feat_table,taskId):
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
    return createPcoa(meta=meta,feat=feat,metric='euclidean',taskId=taskId)
    
    
    


def createPcoa(meta,feat,metric,taskId):
    
    directory_path = os.path.join(os.getcwd(), 'api/static/downloads', str(taskId))
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True) 
    return qiime2PCoA(meta, feat,
                              out_dir=directory_path,
                              metric=metric)
    

     
