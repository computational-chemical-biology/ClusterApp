class FilterByBlankInFilename:
    def __init__(self,df):
        self.df = df

    def execute(self):
        return self.df[self.df['filename'].str.contains('blank') == False]