import salt
import salt.client

from openstack_dashboard.settings import SALT_MASTER_CONFIG
from openstack_dashboard.settings import SALT_SLS_DIR
from openstack_dashboard.settings import SALT_SLS_REPO_DIR


import yaml
from os import listdir


def repo_matrix():

    return {"zypper":["alias",
                             "autorefresh",
                             "baseurl",
                             "cache",
                             "enabled",
                             "gpgcheck",
                             "gpgautoimport",
                             "keeppackages",
                             "mirrorlist",
                             "metadataPath",
                             "name",
                             "packagesPath",
                             "priority",
                             "refresh",
                             "type",
                             "url"],
                      "yum":["baseurl",
                      "comments",
                      "enabled",
                      "failovermethod",
                      "file",
                      "gpgcheck",
                      "gpgkey",
                      "metadata_expire",
                      "mirrorlist",
                      "metalink",
                      "name",
                      "skip_if_unavailable",
                      "file"],
                       "deb":["refresh_db",
                              "dist",
                              "file",
                              "ppa_auth",
                              "keyid",
                              "keyserver",
                              "key_url",
                              "line",
                              "uri",
                              "architectures"
                              "comps",
                              "disabled",
                              "type",
                              "consolidate",
                               "comments"]}





def get_repo_type(repo=None,file_path=None):

    pass

    
                            


def create_repo():

    pass

def remove_repo():

    pass


def edit_repo():

    pass

def get_environment(env_name=None):

    try:

        
        master_config_file = open(SALT_MASTER_CONFIG,"r")
        master_config = yaml.load('\n'.join(master_config_file.readlines()))
        master_config_file.close()
        if env_name == None:
 
            return master_config.get("file_roots",None)

        else:

            environments = master_config.get("file_roots",None)

            if environments!=None:

                return environments.get(env_name,None)

    except OSError:

        print 'No such file or directory: %s'%(SALT_SLS_REPO_DIR)
        return False



def list_repos(env_name=None):


    class EmptyClass():
  
        pass

    try:

        dir_content = []
        dir_content=listdir(SALT_SLS_REPO_DIR)

        
        for repo_file in dir_content:

            pass

        

    except OSError:

        print 'No such file or directory: %s'%(SALT_SLS_REPO_DIR)
        return False

    pass


def subscribe_instance_to_repo():

    pass

def unsubscribe_instance_from_repo():

    pass


def restart_master():

    pass

def mod_master_config():

    pass

def highstate(instance_name="*"):

    info=local.cmd(instance_name,'state.highstate')

    return info
