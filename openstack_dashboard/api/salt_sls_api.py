import salt
import salt.client
import salt.gdc.groups

from openstack_dashboard.settings import SALT_MASTER_CONFIG
from openstack_dashboard.settings import SALT_SLS_DIR
from openstack_dashboard.settings import SALT_SLS_REPO_DIR


import yaml
import operator
from os import listdir
from os.path import isfile,isdir

from openstack_dashboard.dashboards.groups.groupmember import Member,Group

class SlsGoFru_HighLevelKey():

    # Example:
    #   Input:
    #   hash= {'a': {'B': {1: 2}}, 1: 2, 'R': {'b': {'1': 2, 'T': {'a': 1}}}, 'b': {1: 2, 3: {'1': {'3': {'a': 1, '3': 2}}}}, '4': {'3': {1: 2, 3: 4}}}
    #   high_level_key = 'b'
    #   phrase='a'
    #   key_of_incoming_hash = None (always use None)
    #   Output:
    #   {'3': 1, 'T': 1}



    def __init__(self, high_level_key = None  , key_of_incoming_hash = None  ,  hash=None , phrase=None):

        repos_inside_high_level_key=getattr(self,'repos_inside_high_level_key',{})

        if high_level_key == None:

            for key in hash.keys():

                if phrase == key:

                    if key_of_incoming_hash!= None:

                        repos_inside_high_level_key[key_of_incoming_hash] = hash[key]

                elif (isinstance(hash[key], dict)):

                    instance = SlsGoFru_HighLevelKey(high_level_key = None, key_of_incoming_hash = key , hash=hash[key],phrase=phrase)

                    for key in instance.repos_inside_high_level_key.keys():

                        repos_inside_high_level_key[key] = instance.repos_inside_high_level_key[key]

            setattr(self, 'repos_inside_high_level_key', repos_inside_high_level_key)


        else:

            if (isinstance(hash, dict)):

                for key in hash.keys():

                    if (high_level_key == key):

                        instance = SlsGoFru_HighLevelKey(high_level_key = None, key_of_incoming_hash = key , hash=hash[key],phrase=phrase)

                    else:

                        instance = SlsGoFru_HighLevelKey(high_level_key = high_level_key, key_of_incoming_hash = key , hash=hash[key],phrase=phrase)

                    for key in instance.repos_inside_high_level_key.keys():

                        repos_inside_high_level_key[key] = instance.repos_inside_high_level_key[key]

            setattr(self, 'repos_inside_high_level_key', repos_inside_high_level_key)



class SlsGoFru():

    # Example:
    #   Input:
    #   hash= {    'a': {'B': {1: 2}},      1: 2,      'b': {1: 2, 3: {'1': { '3': {'a': 1, '3': 2}  }  } } ,      '4': { '3': {1: 2, 3: 4} }   }
    #   phrase = "3"
    #   key_of_incoming_hash = None (always use None)
    #   Output:
    #   {'1': {'a': 1, '3': 2}, '4': {1: 2, 3: 4}}

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

class DirGoFru():

    def __init__(self, dir_path = None):

        if dir_path != None:

            dir_content=getattr(self,'dir_content',[])

            try:

                content=listdir(dir_path)

            except OSError:

                return dir_files

            for sls_file_name in content:

                full_sls_path = (dir_path+"/"+sls_file_name)

                if isfile(full_sls_path):

                    dir_content.append(full_sls_path)

                elif isdir(full_sls_path):

                    new_dir = DirGoFru(dir_path = full_sls_path).dir_content

                    for file_path in new_dir:

                        dir_content.append(file_path)


            setattr(self, 'dir_content', dir_content)




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



def get_directory_content(dir_path = None):

    if dir_path != None:

        dir_files = []

        try:

            dir_files=DirGoFru(dir_path=dir_path).dir_content

            return dir_files

        except OSError:

            return dir_files
            
            


def list_something_inside_by_key(env_name=None,key_phrase="pkgrepo.managed"):

    """By default as you can see it returns repolists """

    repo_content = []


    try:


        if env_name == None:

            environments = get_environment()
        
            for env in environments:

                for directory in environments[env]:

                    content=get_directory_content(dir_path=directory)

                    for sls_file_name in content:
 
                        sls_file = open(sls_file_name,"r")

                        try:

                            sls_file_data = yaml.load('\n'.join(sls_file.readlines()))

                            sls_file.close()
                        except:

                            sls_file_data = None

                            sls_file.close() 

                        

                        if (isinstance(sls_file_data, dict)):

                            repo_content.append(SlsGoFru(hash=sls_file_data,phrase=key_phrase).found_repos)

        else:

            env_dirs = get_environment(env_name)

            env_files = []

            for env_dir in env_dirs:

                content=get_directory_content(dir_path=env_dir) 

                for env_file in content:

                    env_files.append(env_file)

            for sls_file_name in env_files:
           
                sls_file = open(sls_file_name,"r")

                try:

                    sls_file_data = yaml.load('\n'.join(sls_file.readlines()))

                    sls_file.close()
                except:

                    sls_file_data = None

                    sls_file.close()

                if (isinstance(sls_file_data, dict)):

                    repo_content.append(SlsGoFru(hash=sls_file_data,phrase=key_phrase).found_repos)

        return repo_content 

    except OSError:

        print 'No such file or directory: %s'%(SALT_SLS_REPO_DIR)
        return False


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




def list_instance_repository_subscription(instance_name = None , env_name = None):

    data = []

    environments = get_environment()

    if env_name != None:        

        if environments.get(env_name,None) == None: return []

        environments = {env_name:environments[env_name]}
        

    all_repos_in_all_environments = list_something_inside_by_key(key_phrase="pkgrepo.managed")

    repositories = list_something_inside_by_key(key_phrase="pkgrepo.managed")

    repository_names = []


    for repository in repositories:

        for repository_name in repository.keys():

            repository_names.append(repository_name)

      

    for env in environments:


        for directory in environments[env]:

            content=get_directory_content(dir_path=directory)

            for sls_file_name in content:

                sls_file = open(sls_file_name,"r")

                try:

                    sls_file_data = yaml.load('\n'.join(sls_file.readlines()))

                    sls_file.close()

                except:

                    sls_file_data = None

                    sls_file.close()

                    continue

                if (isinstance(sls_file_data, dict)):
                        
                    collected_data = (SlsGoFru(hash=sls_file_data,phrase=instance_name).found_repos)

                    instance_repository_set = []

                    if (collected_data not in data) and (collected_data!={}):


                        if (collected_data.get(env,None)!=None):

                            for repository_highlevel_name in collected_data[env]:

                               
                                if repository_highlevel_name not in repository_names:

                                    for directory in environments[env]: 

                                        content=get_directory_content(dir_path=directory) 


                                        for sls_file_name in content:

                                            sls_file = open(sls_file_name,"r")

                                            try:

                                                sls_file = open(sls_file_name,"r")

                                                sls_file_data = yaml.load('\n'.join(sls_file.readlines()))

                                                sls_file.close()

                                            except:

                                                sls_file_data = None

                                                sls_file.close()

                                                continue
 
                                                 
                                            if (isinstance(sls_file_data, dict)):

                                                instance = SlsGoFru_HighLevelKey(high_level_key = repository_highlevel_name , hash=sls_file_data , phrase="pkgrepo.managed")
 

                                                for key in instance.repos_inside_high_level_key.keys():

                                                    instance_repository_set.append(key)
                                                   
 
                                else:

                                    instance_repository_set.append(repository_highlevel_name)

                            data.append({env:instance_repository_set})                   


    return data


def get_groups_sls():

    gm = salt.gdc.groups.GdcMatcher()
    groups = gm.get_groups()

    group_instances = []
    for group in groups:

        group_instances.append(Group(member_group_name=group,members=gm.get_by_group(group)))

    return group_instances

def get_group_members_sls(group_name):

    gm = salt.gdc.groups.GdcMatcher()

    members = gm.get_by_group(group_name)

    member_instances = []

    for member in members:

        member_instances.append(Member(member_name=member,member_group_names=gm.get_by_host(member)))

    return member_instances




def minions_list_sls():

    gm = salt.gdc.groups.GdcMatcher()

    return gm.get_all_hosts()

def get_members_sls_custom():

    gm = salt.gdc.groups.GdcMatcher()

    member_list = []

    for member_name in minions_list_sls():


        member_list.append(Member(member_name = member_name,
                                      member_group_names = gm.get_by_host(member_name)))


    return member_list

def get_group_members_simple_sls(group_name=None):

    gm = salt.gdc.groups.GdcMatcher()

    member_list = []

    for member_name in gm.get_by_group(group_name):


        member_list.append(member_name)


    return member_list


def get_member_sls(member_name=None):

    member_groups = []

    if member_name!= None:

        gm = salt.gdc.groups.GdcMatcher()
        member_groups = gm.get_by_host(member_name)
        

    return Member(member_name=member_name,member_group_names=member_groups)

def update_member_sls(member_name=None,member_type='instance',member_group_names=[]):

    gm = salt.gdc.groups.GdcMatcher()

    current_member_groups = gm.get_by_host(member_name)

    add_group = []

    remove_group = []


    for new_group in member_group_names:

        if new_group not in current_member_groups:

            add_group.append(new_group)

    for old_group in current_member_groups:

        if old_group not in member_group_names:

            remove_group.append(old_group)

    for group in add_group:

            print '>> join'
            print member_name.encode('ascii', 'ignore')
            print group
            print add_group
            print '======='

            gm.join_to_group([member_name.encode('ascii', 'ignore')],group.encode('ascii', 'ignore'))

    for group in remove_group:


            print '>> remove'

            print member_name.encode('ascii', 'ignore')
            print group
            print remove_group
            print '======='
            gm.remove_from_group([member_name.encode('ascii', 'ignore')],group.encode('ascii', 'ignore'))


    print '>> new_group'
    print add_group
    print '>> old_group'
    print remove_group
    print '------------'
    
    return gm.get_by_host(member_name)

    

        
def del_group(group_name=None):

    gm = salt.gdc.groups.GdcMatcher()    
    gm.del_group([group_name])

def remove_everywhere(member_name=None):

    gm = salt.gdc.groups.GdcMatcher()
    gm.remove_everywhere([member_name])

def create_group_sls(group_name=None):

    gm = salt.gdc.groups.GdcMatcher()
    gm.add_group({group_name.encode('ascii', 'ignore'):''})

            

    


