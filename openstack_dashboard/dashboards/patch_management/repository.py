class DebRepository():

    def __init__(self, id = None, architectures=None, comps=None, disabled=None ,dist=None, repo_file=None,line=None,repo_type=None,uri=None):

        self.id = id
        self.architectures = architectures
        self.comps = comps
        self.disabled = disabled
        self.dist = dist
        self.repo_file = repo_file
        self.line = line
        self.repo_type = repo_type
        self.uri = uri

class RpmRepository():

    repo_list=[]

    def __init__(self, id = None, comments=None, enabled=None, failovermethod=None ,repo_file=None, gpgcheck=None, gpgkey=None , metadata_expire=None,metalink=None, name=None, skip_if_unavailable=None):

        self.id = id
        self.comments = comments
        self.enabled = enabled
        self.failovermethod = failovermethod
        self.repo_file = repo_file
        self.gpgcheck = gpgcheck
        self.gpgkey = gpgkey
        self.metadata_expire = metadata_expire
        self.metalink = metalink
        self.name = name
        self.skip_if_unavailable = skip_if_unavailable

        self.repo_list.append(id)


