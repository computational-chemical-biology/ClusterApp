class MetaFeatDto:

    def __init__(self, feat, meta):
        self.feat = feat
        self.meta = meta

    def to_dict(self):
        return {
            "feat": self.feat,
            "meta": self.meta,
        }