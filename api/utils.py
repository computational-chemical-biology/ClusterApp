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

     
