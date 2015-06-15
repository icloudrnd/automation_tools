#
# salt api wrapper for horizon dashboard
#
# 
#
import salt
import salt.config
from salt import runner
import salt.ext.gdc_groups

#
from openstack_dashboard.settings import SALT_MASTER_CONFIG
#
# Determine package management system type 
#
from openstack_dashboard.settings import OS_PACKAGE_SPEC
#
#
opts = salt.config.master_config(SALT_MASTER_CONFIG)
#
#
# database for completed tasks 
from openstack_dashboard.dashboards.tasks.models import SaltReturns
from openstack_dashboard.dashboards.groups.models import GroupMember
#
#
##
from openstack_dashboard.dashboards.tasks.task import ActiveTask
##
from openstack_dashboard.dashboards.patch_management.package import Package as Patch_Package
##
from openstack_dashboard.dashboards.patch_management.package import Instance as Patch_Instance
#
from openstack_dashboard.dashboards.patch_management.repository import DebRepository, RpmRepository
##
from horizon import exceptions
from django.utils.translation import ugettext_lazy as _
#
#

def active_jobs():

    runner = salt.runner.RunnerClient(opts)

    
    active_task_list = []
 
    try:
 
        active_tasks_list = runner.cmd('jobs.active', [])

    except:

        raise exceptions.NotAvailable(_('Salt-master is not available'))
 

    active_task_list_converted  = []
    #  bug is here 

    for task_id in active_tasks_list.keys():

        single_active_task = active_tasks_list[task_id]

        active_task_list_converted.append( ActiveTask( id=task_id, 
                                                       function=single_active_task['Function'] , 
                                                       user=single_active_task['User'], 
                                                       target_type=single_active_task['Target-type'], 
                                                       returned=single_active_task['Returned'], 
                                                       running_on=single_active_task['Running'], 
                                                       arguments=single_active_task['Arguments'] ))


    return active_task_list_converted

def delete_task(jid,scope='*'):

    local = salt.client.LocalClient()

    try:

        local.cmd(scope, 'saltutil.kill_job', [jid])

    except:

        raise exceptions.NotAvailable(_('Unable to delete task %s'%(str(jid))))


def pkg_list_for_upgrade(instance_name=None):

    local = salt.client.LocalClient()

    pkg_list=local.cmd(instance_name,'pkg.list_upgrades')

    pkg_list_m = []

    pkg_list = pkg_list[instance_name]
 
    for i in pkg_list.keys():

        pkg_list_m.append(Patch_Package(name=i,version=pkg_list[i]))
    
    
    return pkg_list_m

def get_grains(instance_name=None,*args):

    local = salt.client.LocalClient()

    grains_names=list(args)

    grains_list = local.cmd(instance_name,'grains.item',grains_names)

    return grains_list[instance_name]

def minions_list():

     runner = salt.runner.RunnerClient(opts)

     minions_list = runner.cmd('manage.up', [])

     return minions_list

def minions_list_fast():

     gm = salt.ext.gdc_groups.GdcMatcher()

     return gm.get_all_hosts()

def minions_list_custom():

    """Minions list table with os column """

    minions_list_base = minions_list_fast()

    minions_list_m = []

    GRAIN_NAME = 'os'

    for instance_name in minions_list_base:

        os = get_grains(instance_name,GRAIN_NAME)[GRAIN_NAME]

        minions_list_m.append(Patch_Instance(name=instance_name, os=os))

    return minions_list_m

def install_packages(instance_name=None,packages=[]):

    local = salt.client.LocalClient()

    PKG_INSTALL = "pkg.install" 

    return local.run_job(instance_name,PKG_INSTALL,["""pkgs='%s'"""%(str(packages).replace("'",'"'))])

def add_zypper_repo(instance_name=None, repo = None ,  baseurl = None , enabled = None , refresh=None , cache = None , gpgcheck = None , gpgautoimport=None ):

    local = salt.client.LocalClient()

    MOD_REPO = "pkg.mod_repo"

    local.run_job(instance_name,MOD_REPO,[repo],kwarg={'baseurl': baseurl, #'repo': repo,
                                                       'url': baseurl,
                                                       'enabled': enabled,
                                                       'refresh':refresh ,
                                                       'cache':cache , 
                                                       'gpgcheck':gpgcheck ,
                                                       'gpgautoimport':gpgautoimport })

def add_yum_repo(instance_name = None, repo = None , name = None , baseurl = None , mirrorlist = None ):

    local = salt.client.LocalClient()

    MOD_REPO = "pkg.mod_repo"

    local.run_job(instance_name,MOD_REPO ,[repo],kwarg={ 'name': name , 
                                                         'baseurl': baseurl })

def get_repo_list_rpm(package_manager=None):

    class EmptyClass():

        pass


    local = salt.client.LocalClient()

    GRAIN_NAME = 'os'

    minions_objects = minions_list_custom()

    rpm_based_machines_names = []

    repo_fields = {
              "zypper":["alias","autorefresh","baseurl","cache","enabled","gpgcheck","gpgautoimport","keeppackages","mirrorlist","metadataPath","name","packagesPath","priority","refresh","type","url"],
              "yum":["baseurl","comments","enabled","failovermethod","file","gpgcheck","gpgkey","metadata_expire","mirrorlist","metalink","name","skip_if_unavailable","file"] }

    if package_manager == None: package_manager="rpm"

    for machine in minions_objects:

        if machine.os in OS_PACKAGE_SPEC[package_manager]:

            rpm_based_machines_names.append(machine.id)
    

    instance_list=','.join(rpm_based_machines_names)

    repositories = {}

    for instance_name in rpm_based_machines_names:

        instance_repo_list=local.cmd(instance_name,'pkg.list_repos')

        repository_set = instance_repo_list[instance_name]

        if type(repository_set) == type("Hello world !"): break

        for key in repository_set.keys():

            current_repo  = repository_set[key]

            repo_instance = EmptyClass()

            if key not in repositories.keys():


                setattr(repo_instance,'id',key)
                setattr(repo_instance,'instances',[instance_name])

                for field in repo_fields[package_manager]:
   
                    setattr(repo_instance,field,current_repo.get(field,""))
                
                repositories[key]=repo_instance

            else:

                
                current_repo_clients = getattr(repositories[key],'instances')
                current_repo_clients.append(instance_name)
                
                setattr(repositories[key],'instances',current_repo_clients)


    return repositories.values()


def get_repo_list_deb():

    local = salt.client.LocalClient()

    GRAIN_NAME = 'os'

    minions_objects = minions_list_custom()

    deb_based_machines_names = []

    for machine in minions_objects:

        if machine.os in OS_PACKAGE_SPEC["deb"]:

            deb_based_machines_names.append(machine.id)

    #OS_PACKAGE_SPEC["deb"]


    instance_list=','.join(deb_based_machines_names)

    repositories = []

    uniq_repository_names = []

    for instance_name in deb_based_machines_names:

        instance_repo_list=local.cmd(instance_name,'pkg.list_repos')

        repository_set = instance_repo_list[instance_name]

        if type(repository_set) == type("Hello world !"): break

        for key in repository_set.keys():


            current_repo  = repository_set[key]

            current_repo=current_repo[0]


            if key not in uniq_repository_names:

                uniq_repository_names.append(key)

                repositories.append(DebRepository(id = key,
                                                  architectures = current_repo.get("architectures",""),
                                                  comps=current_repo.get("comps",""),
                                                  disabled=current_repo.get("disabled",""),
                                                  dist=current_repo.get("dist",""),
                                                  repo_file=current_repo.get("file"),
                                                  line=current_repo.get("line",""),
                                                  repo_type=current_repo.get("type",""),
                                                  uri=current_repo.get("uri","")))





    return repositories



def grains_ls():

    local = salt.client.LocalClient()
    instances_hash=local.cmd('*','grains.ls')
    grains = []
    for key in instances_hash:
        for grain in instances_hash[key]:
            if grain not in grains:
                grains.append(grain)
    return grains

def match_by_grain(grain=None,value=None):

    local = salt.client.LocalClient()

    instances_list=local.cmd(str(grain+":"+value),'test.ping',expr_form='grain')

    return instances_list.keys()

def add_rpm_repo(grain_hash={}):
    local = salt.client.LocalClient()
    pass

def join_scope(scope=[]):

    hash={}

    for subscope in scope:

        for item in subscope:
 
            hash[item]=1

    return hash.keys()

def collect_scope(grainpairs=[]):

    # grainpairs ==  [u'os:Ubuntu', u'os:openSUSE']

    for grainpair in grainpairs:

        pass

