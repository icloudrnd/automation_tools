class Package():

    def __init__(self, name = None, version=None):
        self.id = name
        self.version = version


class Instance():

    def __init__(self, name = None, os=None):

        self.id = name
        self.os = os
