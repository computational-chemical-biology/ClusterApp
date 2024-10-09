class FilterByBlankInFilename:
    def __init__(self,df):
        self.df = df

    def execute(self):
        self.df.columns = self.df.columns.str.replace('Filename', 'filename')
        return self.df[~self.df['filename'].str.contains('blank', case=False, na=False)]
