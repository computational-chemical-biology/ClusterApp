import pandas as pd

from api.src.model.FilterBlanks import FilterBlanks


class FilterByBlanks:
    def __init__(self,df,filterBlanks: FilterBlanks):
        self.df = df
        self.filterBlanks = filterBlanks

    def execute(self):
        return self.filterBlank(self.df, self.filterBlanks.propBlankFeats, self.filterBlanks.propSamples)
    
    def filterBlank(self,feat_table, prop_blank_feats=1.0, prop_samples=0.9):
        """Filters out features that have intensity less than a desired
        proportion of intensity in blank samples at a given
        number of samples
        Parameters
        ----------
        feat_table: pd.DataFrame
            DataFrame containing columns with ATTRIBUTE_ suffix.
            Blank samples should contain "B(b)lank" in the name
        prop_blank_feats: float
            Proportion of blank intensity that a feature has to be greater to be kept.
        prop_samples: float
            Proportion of samples in which the feature has to be greated than blank average proportion.
        Returns
            Filtered pd.DataFrame.
        -------
        """
        
        prop_blank_feats = float(prop_blank_feats)
        prop_samples = float(prop_samples)

        feat_table.rename(columns={'Filename': 'filename'}, inplace=True)

        last_attr = feat_table.columns[feat_table.columns.str.contains('ATTRIBUTE')][-1]
        plast_attr = feat_table.columns.get_loc(last_attr)+1
        mask = feat_table.filename.str.lower().str.contains('blank')
        if self.isValidToFilter(feat_table):
            return {
            'dataframe': self.df,
            'description': f'No blank samples found in the provided data.',
            'isFiltered': False
            }

        blank_mean = feat_table.loc[mask, feat_table.columns[plast_attr:]].mean()
        feat_less_blank = (feat_table.loc[~mask, feat_table.columns[plast_attr:]]>(prop_blank_feats*blank_mean)).sum()
        prop_feat_less_blank = feat_less_blank > prop_samples*(feat_table.shape[0]-mask.sum())
        nprop = prop_feat_less_blank.sum()
        return {
            'dataframe': pd.concat([feat_table.loc[~mask, feat_table.columns[:plast_attr]],
                        feat_table.loc[~mask, prop_feat_less_blank[prop_feat_less_blank].index]], axis=1),
            'description': f'Filtered out {nprop} features whose intensity was less than {prop_blank_feats*100}% of the average intensity of blank samples in {prop_samples*100}% samples at least.',     
            'isFiltered': True
            }
    

    def isValidToFilter(self,feat_table):
        feat_table_copy = feat_table.copy()
        feat_table_copy['filename'] = feat_table_copy['filename'].fillna('')
        return feat_table_copy['filename'].str.lower().str.contains('blank').sum() == 0