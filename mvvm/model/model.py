class BaseModel:
    pass


class GraphBuilderModel(BaseModel):
    def __init__(self):
        self._dummy = None

    @property
    def dummy(self):
        return self._dummy

    @dummy.setter
    def dummy(self, value):
        self._dummy = value
