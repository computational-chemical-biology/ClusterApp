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

def filterBlank(feat_table, prop_blank_feats=1.0, prop_samples=0.9):
    """Filters out features that have intensity less than a desired
       proportion of intensity in blank samples at a given
       number of samples
    Parameters
    ----------
    feat_table: pd.DataFrame
        DataFrame containing columns with ATTRIBUTE_ suffix.
        Blank samples should contain "B(b)lank" in the name
    prop_blank_feats: float
        Proportion of blank intensitie that a feature has to be greater to be keept.
    prop_samples: float
        Proportion of samples in which the feature has to be greated than blank average proportion.
    Returns
        Filtered pd.DataFrame.
    -------
    """
    last_attr = feat_table.columns[feat_table.columns.str.contains('ATTRIBUTE')][-1]
    plast_attr = feat_table.columns.get_loc(last_attr)+1
    mask = feat_table.filename.str.lower().str.contains('blank')
    print('Found %s samples containing "blank" in the name.' % mask.sum())
    print('Found %s features.' % (feat_table.shape[1]-plast_attr))
    blank_mean = feat_table.loc[mask, feat_table.columns[plast_attr:]].mean()
    feat_less_blank = (feat_table.loc[~mask, feat_table.columns[plast_attr:]]>(prop_blank_feats*blank_mean)).sum()
    prop_feat_less_blank = feat_less_blank > prop_samples*(feat_table.shape[0]-mask.sum())
    nprop = prop_feat_less_blank.sum()
    print(f'''Found {nprop} features whose intensity was greater than {prop_blank_feats*100}% of the
          average intensity of blank samples in {prop_samples*100}% samples at least.''')
    return pd.concat([feat_table.loc[~mask, feat_table.columns[:plast_attr]],
                      feat_table.loc[~mask, prop_feat_less_blank[prop_feat_less_blank].index]], axis=1)


def createPcoa(meta,feat,metric):
    taskid = uuid.uuid4()
    if not os.path.exists(f'api/static/downloads/{taskid}'):
            os.mkdir(f'api/static/downloads/{taskid}')
    return qiime2PCoA(meta, feat,
                              out_dir=f'api/static/downloads/{taskid}',
                              metric=metric)
     
