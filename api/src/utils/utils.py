import os
import re
import pandas as pd
import numpy as np
from api.src.model.DataProcessingConfig import DataProcessingConfig
from api.src.service.factorys.normalization.NormalizationFactory import NormalizationFactory
from api.src.service.factorys.ScalingFactory import ScalingFactory
import qiime2
from qiime2 import Artifact
from qiime2.plugins import metadata, feature_table, diversity, emperor
from q2_emperor import plot, procrustes_plot, biplot, generic_plot
from scipy.spatial.distance import squareform, pdist
import skbio
import uuid


def qiime2PCoA(sample_metadata, df, out_dir,dataProcessingConfig:DataProcessingConfig):
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


    if dataProcessingConfig.normalization != None:
        df2 = NormalizationFactory(dataProcessingConfig.normalization).normalize(df2)
         
    if dataProcessingConfig.scaling != None:
        df2 = ScalingFactory(dataProcessingConfig.scaling).scale(df2)

    df2.fillna(0, inplace=True)
    zero_proportion = (df2 == 0).sum().sum() / df2.size

    if zero_proportion == 1.0: 
        raise ValueError(f"The DataFrame contains too many zero values ({zero_proportion:.2%}). Please check the input data table or try different scaling and normalization methods.")

    dm1 = squareform(pdist(df2, metric=dataProcessingConfig.metric))
    dm1 = skbio.DistanceMatrix(dm1, ids=df2.index.tolist())
    dm1 = Artifact.import_data("DistanceMatrix", dm1)
    pcoa = diversity.methods.pcoa(dm1)
    emperor_plot = emperor.visualizers.plot(pcoa.pcoa, qsample_metadata)

    if '.qzv' in out_dir:
        emperor_plot.visualization.save(out_dir)
    else:
        emperor_plot.visualization.export_data(out_dir)
    return emperor_plot


def createFile(request,session,app):
    file = None
    for key, f in request.files.items():
        file = f
    if file is None:
        return '', 400
        
        
    if not os.path.exists(app.config['UPLOADED_PATH']):
        os.makedirs(app.config['UPLOADED_PATH'], exist_ok=True)    

    fileId = str(uuid.uuid4())
    session['fileId'] = fileId
    file.save(os.path.join(app.config['UPLOADED_PATH'], fileId))


def getFile(session,app):
    fileId = session.get('fileId')
    if fileId is None:
        return None
        
    return os.path.join(app.config['UPLOADED_PATH'], fileId)

     
