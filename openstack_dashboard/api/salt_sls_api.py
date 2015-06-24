import salt
import salt.client

from openstack_dashboard.settings import SALT_MASTER_CONFIG
from openstack_dashboard.settings import SALT_SLS_DIR
from openstack_dashboard.settings import SALT_SLS_REPO_DIR


import yaml
import operator
from os import listdir
from os.path import isfile

class SlsGoFru():

    def __init__(self, key_of_incoming_hash  = None  ,  hash=None , phrase=None):

        found_repos=getattr(self,'found_repos',{})

        for key in hash.keys():

            if phrase == key:

                if key_of_incoming_hash!= None:

                    found_repos[key_of_incoming_hash] = hash[key]

            elif (isinstance(hash[key], dict)):

                instance = SlsGoFru(key_of_incoming_hash = key , hash=hash[key],phrase=phrase)

                for key in instance.found_repos.keys():

                    found_repos[key] = instance.found_repos[key]

        setattr(self, 'found_repos', found_repos)



def get_repo_matrix():

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

def sls_is_repofile(sls_file_hash=None):

    if sls_file_hash == None:

        return False

    table = {"zypper":0,"yum":0,"deb":0}
    repo_matrix = get_repo_matrix()

    for repo_type in repo_matrix:

        if repo_type == "zypper":

            for repo_key in repo_matrix[repo_type]:

                if repo_key in sls_file_hash:

                    table[repo_type]+=1

   
        if repo_type == "yum":

            for repo_key in repo_matrix[repo_type]:

                if repo_key in sls_file_hash:

                    table[repo_key]+=1

        if repo_type == "deb":

            for repo_key in repo_matrix[repo_type]:

                if repo_key in sls_file_hash:

                    table[repo_key]+=1

        
        sorted_table = sorted(table.items(), key=operator.itemgetter(1))
        (repo_name,count)=sorted_table.pop()
        if count == 0:
            return False
        else:
            return repo_name


         
     
              

            

    
    



    
                            


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

        if env_name == None:

            environments = get_environment()
        
            for env in environments:

                for directory in environments[env]:

                    content=listdir(directory)

                    for sls_file_name in content:

                        full_sls_path = (directory+"/"+sls_file_name) 

                        if isfile(full_sls_path):
 
                            sls_file = open(full_sls_path,"r")

                            sls_file_data = yaml.load('\n'.join(sls_file.readlines()))

                            if (isinstance(sls_file_data, dict)):

                                for data in sls_file_data.keys():

                                    if (isinstance(sls_file_data[data], dict)):
     
                                        for key in sls_file_data[data]:

                                            print key
                                            
                                            if sls_is_repofile(data[key]) != False:

                                                dir_content.append({sls_is_repofile(data[key]):data[key]})

                                                                   




        else:
             env_path = get_environment(env_name)
             dir_content=listdir(env_path)

             for repo_file in dir_content:
           
                 sls_file = open(env_path+"/"+repo_file)
                 sls_file_data = yaml.load('\n'.join(sls_file.readlines()))

            

        return dir_content 

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
