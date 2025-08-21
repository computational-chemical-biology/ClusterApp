from scipy.spatial.distance import squareform, pdist
import skbio
import re
import pandas as pd
from api.src.model.dto.MetaFeatDto import MetaFeatDto
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class CreatePlotsService:
    def __init__(self, metaFeatDto: MetaFeatDto, uuid):
        self.metaFeatDto = metaFeatDto
        self.uuid = uuid

    def create(self):
        distance_matrix = self._prepare_distance_matrix()
        pcoa = skbio.stats.ordination.pcoa(distance_matrix)
        tpcoa = pd.merge(self.metaFeatDto.meta.reset_index()[['#SampleID','ATTRIBUTE_Gender']],
        pcoa.samples.reset_index(),
        left_on='#SampleID', right_on='index')
        
        scatterPlot = self._create_scatter_plot(tpcoa=tpcoa,pcoa=pcoa)
        screePlot = self._create_scree_plot(pcoa)
        pairPlot = self._create_pair_plot(tpcoa)
        clustersPlot = self._create_clusters_plot(pcoa)

        return {
            "scatterPlot": scatterPlot,
            "screePlot": screePlot,
            "pairPlot": pairPlot,
            "clustersPlot": clustersPlot
        }

    def _prepare_distance_matrix(self):
        sample_metadata, df = self.metaFeatDto.meta, self.metaFeatDto.feat
        sample_metadata.rename(index=str, columns={"filename": "#SampleID"},
                            inplace=True)
        sample_metadata.columns = sample_metadata.columns.str.replace('\s', '_')

        sample_metadata.index = sample_metadata['#SampleID']
        sample_metadata.drop(['#SampleID'], axis=1, inplace=True)

        df2 = df[df.columns[df.columns.str.contains(' Peak area')]]
        df2.columns = [re.sub('(.+\.mzX?ML) .+', '\\1', a) for a in df2.columns]
        df2.index = df['row ID'].astype(str)
        df2 = df2.T

        df2.fillna(0, inplace=True)
        zero_proportion = (df2 == 0).sum().sum() / df2.size

        if zero_proportion == 1.0: 
            raise ValueError(f"The DataFrame contains too many zero values ({zero_proportion:.2%}). Please check the input data table or try different scaling and normalization methods.")

        dm1 = squareform(pdist(df2, metric='canberra'))
        dm1 = skbio.DistanceMatrix(dm1, ids=df2.index.tolist())
        return dm1

    def _create_scatter_plot(self, tpcoa,pcoa):
        sns.scatterplot(data=tpcoa, x="PC1", y="PC2", hue="ATTRIBUTE_Gender")
        plt.xlabel("PCo 1 ({:.2f}%)".format(round(pcoa.proportion_explained[0], 4)*100))
        plt.ylabel("PCo 2 ({:.2f}%)".format(round(pcoa.proportion_explained[1], 4)*100))
        name = f'pcoa2d_plot_{self.uuid}.png'
        plt.savefig(name)
        return name

    def _create_scree_plot(self, pcoa):
        fig, ax = plt.subplots()
        PC_values = np.arange(5) + 1
        plt.plot(PC_values, pcoa.proportion_explained[:5], 'o--', linewidth=2, color='blue')
        plt.title('Scree Plot')
        plt.xlabel('Principal Component')
        plt.ylabel('Variance Explained')
        ax.set_xticks(PC_values)
        name = f'scree_plot_{self.uuid}.png'
        plt.savefig(name)
        return name
        

    def _create_pair_plot(self, tpcoa):
        sns.pairplot(tpcoa[['ATTRIBUTE_Gender',	'PC1', 'PC2', 'PC3']], hue="ATTRIBUTE_Gender")
        name = f'pcoa_pair_plot_{self.uuid}.png'
        plt.savefig(name)
        return name

    def _create_clusters_plot(self, pcoa):
        range_n_clusters = [2, 3, 4, 5, 6]
        silhouette_list = []

        for n_clusters in range_n_clusters:
            clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(pcoa.samples[['PC1', 'PC2', 'PC3', 'PC4', 'PC5']])

            silhouette_avg = silhouette_score(pcoa.samples[['PC1', 'PC2', 'PC3', 'PC4', 'PC5']], cluster_labels)
            silhouette_list.append(silhouette_avg)
            
        fig ,ax = plt.subplots()
        plt.plot([2, 3, 4, 5, 6], silhouette_list, linestyle='dashed')
        plt.scatter([2, 3, 4, 5, 6], silhouette_list)
        ax.set_xticks([2, 3, 4, 5, 6])
        plt.xlabel('Number of clusters')
        plt.ylabel('Silhouette average')
        name = f'clusters_plot_{self.uuid}.png'
        plt.savefig(name)
        return name