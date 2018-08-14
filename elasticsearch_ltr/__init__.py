from .client import ElasticsearchLTR


class Model(object):
    def __init__(self, name, type, definition):
        self.name = name
        self.type = type
        self.definition = definition
