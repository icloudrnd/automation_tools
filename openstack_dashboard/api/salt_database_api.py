#
#
#
from openstack_dashboard.dashboards.tasks.models import SaltReturns
from openstack_dashboard.dashboards.groups.models import GroupMember
#
#
from openstack_dashboard.dashboards.tasks.task import CompletedTask, Instance
from openstack_dashboard.dashboards.groups.groupmember import Member,Group
#
#
from horizon import exceptions
from horizon.utils import functions as utils
#
from django.utils.translation import ugettext_lazy as _



def event_types():

    try:

        functions = list(SaltReturns.objects.values_list('fun', flat=True).distinct())

    except:

        raise exceptions.NotAvailable(_('Database connection is not available'))

    return functions

def functions_and_jids(): 

    try:

        return list(SaltReturns.objects.order_by('jid').distinct('jid').values('jid','fun'))

    except:

        raise exceptions.NotAvailable(_('Database connection is not available'))

  

    

    

def task_body(job_id,scope='*'):


    try:

        job_body_db_request = SaltReturns.objects.filter(jid=job_id)

    except:

        raise exceptions.NotAvailable(_('Database connection is not available'))

    

    job_body=job_body_db_request.values()[0]


    return CompletedTask(id = job_body['jid'], 
                         function=job_body['fun'], 
                         added=job_body['added'], 
                         success=job_body['success'], 
                         return_field=job_body['return_field'], 
                         scope=job_body['id'])

def task_body_harp(job_id):

    class Data():

        def __init__(self,id=None,return_field=None,function=None,success=None):

            self.id = id
            self.return_field = return_field
            self.function = function
            self.success = success

        def split_return_field(self):

            return [ i for i in str(self.return_field).split("\\n")]


    try:

        job_body_db_request = SaltReturns.objects.filter(jid=job_id).values()

    except:

        raise exceptions.NotAvailable(_('Database connection is not available'))

    

    job_body_db_request_first = job_body_db_request[0]

    collection = list(Data(id = entry['id'] , 
                           return_field = entry['return_field'] ,
                           function=entry['fun'],
                           success=entry['success'] ) for entry in job_body_db_request )

    return CompletedTask(id = job_id, function=job_body_db_request_first['fun'], added=job_body_db_request_first['added'],
                         collection = collection)







def get_nrecords(page_number,page_count):

    page_number = int(page_number)

    page_count = int(page_count)

    pages_end = page_number*page_count

    pages_start = pages_end - page_count

    pages_returned = SaltReturns.objects.order_by('added').reverse()[pages_start:pages_end]

    return pages_returned

def get_all_records():


    completed_task_array_converted=[]


    try:

        completed_task_array = SaltReturns.objects.order_by('jid').distinct('jid').reverse()

        for entry in completed_task_array.values('jid','added','success','fun'):


            completed_task_array_converted.append(CompletedTask(id=entry["jid"],
                                              function=entry["fun"],
                                              added=str(entry["added"]) ,
                                              success=None,
                                              return_field=None,
                                              scope=None))


    except:

        raise exceptions.NotAvailable(_('Database connection is not available')) 


    has_more_data = True
    return completed_task_array_converted



def get_all_records_mod(request,paginate=False,marker=None):


    completed_task_array_converted = []

    page_size = utils.get_page_size(request)

    limit = None

    if paginate:

        limit = page_size + 1

    has_more_data = False

    try:

        marker_position = None

        if marker!=None:

            sorted_jids = SaltReturns.objects.order_by('jid').distinct('jid').reverse().values('jid')

            marker_position = list(sorted_jids).index({'jid': unicode(marker)}) + 1

        else:
   
            marker_position = 0


        if limit == None:

            completed_task_array = SaltReturns.objects.order_by('jid').distinct('jid').reverse()
 
        else:

            completed_task_array = SaltReturns.objects.order_by('jid').distinct('jid').reverse()[marker_position:limit+marker_position]


        for entry in completed_task_array.values('jid','added','success','fun'):


            completed_task_array_converted.append(CompletedTask(id=entry["jid"],
                                              function=entry["fun"],
                                              added=str(entry["added"]) ,
                                              success=None,
                                              return_field=None,
                                              scope=None))


        if paginate and len(completed_task_array_converted) > page_size:


            completed_task_array_converted.pop(-1)

            has_more_data = True



    except:

        raise exceptions.NotAvailable(_('Database connection is not available'))


    return (completed_task_array_converted,has_more_data)





def get_entries_count(server_name=False):

    if(server_name==False):

        return SaltReturns.objects.count()

    else:
        server_name=str(server_name)

        return SaltReturns.objects.filter(id=server_name).count()




def instances_list():

    return list(SaltReturns.objects.order_by('id').distinct('id').values('id'))

def get_last_update_for_instance(iname=None):

    return SaltReturns.objects.order_by('added').reverse().filter(id=iname)[0:1].values()

def fill_history():

    instance_list = []

    for instance in instances_list():

        instance_data = get_last_update_for_instance( iname = instance['id'] )

        instance_data = instance_data[0]

        instance_list.append(Instance(id=instance['id'], 
                                      function = instance_data['fun'],
                                      added = instance_data['added'],
                                      success = instance_data['success'],
                                      active_tasks = None ) )

    return instance_list 



def create_member(member_name=None,member_type=None,member_group_names=[]):

    if (member_group_names):

        for group in member_group_names:        

            if (GroupMember.objects.filter(member_group_name=group).distinct('member_group_name')):

                new_member = GroupMember.objects.create(member_name=member_name,member_type=member_type,member_group_name=group)
    
                new_member.save()

    else:

        new_member = GroupMember.objects.create(member_name=member_name,member_type=member_type)

        new_member.save()





def update_member(member_name=None,member_type=None,member_group_names=[]):

    member_type=member_type.split("'")[1]
    
    valid_group_list = []

    for group in member_group_names:

        for entry in GroupMember.objects.filter(member_group_name=group).distinct('member_group_name'):

            valid_group_list.append(entry)


    if not valid_group_list and member_group_names!=[]:

        GroupMember.objects.filter(member_name=member_name).update(member_type=member_type)

        print valid_group_list

        return None

    if member_group_names == []:

        GroupMember.objects.filter(member_name=member_name).filter(member_type=member_type).delete()
        GroupMember.objects.create(member_name=member_name,member_type=member_type)

        return None
         

    if GroupMember.objects.filter(member_name=member_name).filter(member_type=member_type).distinct('member_name'):

        GroupMember.objects.filter(member_name=member_name).filter(member_type=member_type).delete()

        for group in member_group_names:

            if GroupMember.objects.filter(member_group_name=group).distinct('member_group_name'):

                new_member = GroupMember.objects.create(member_name=member_name,member_type=member_type,member_group_name=group)

                new_member.save()


def create_member_group(member_group_name=None):

    if not GroupMember.objects.filter(member_group_name=member_group_name).distinct('member_group_name'):

        new_member = GroupMember.objects.create(member_group_name=member_group_name)

        new_member.save()

    else:

        raise exceptions.Conflict(_('Group with name %s is already exist'%(member_group_name)))


def remove_member(member_name=None,member_type=None):

    GroupMember.objects.filter(member_name=member_name).filter(member_type=member_type).delete()

def remove_group(member_group_name=None):

    GroupMember.objects.filter(member_group_name=member_group_name).filter(member_type='').filter(member_name='').delete()

    GroupMember.objects.filter(member_group_name=member_group_name).update(member_group_name='')

def remove_member(member_name=None):

    if (member_name is not u'' ) and (member_name is not '') and (member_name):

        GroupMember.objects.filter(member_name=member_name).delete()


def get_members():

    return GroupMember.objects.distinct('member_name').values('member_name')


def get_member_groups(member_name=None):

    member_groups = []

    for group_object in GroupMember.objects.filter(member_name=member_name).values('member_group_name').distinct('member_group_name'):

        if (group_object['member_group_name'] is not u'') and ( group_object['member_group_name'] is not ''):

            member_groups.append(group_object['member_group_name'])

    return member_groups


    

def get_group_members(member_group_name=None):


    group_members = []

    for member_object in GroupMember.objects.filter(member_group_name=member_group_name).values('member_name').distinct('member_name'):

        if (member_object['member_name'] is not u'') and ( member_object['member_name'] is not '' ):

            group_members.append(member_object['member_name'])


    return group_members

def get_group_members_wrap(member_group_name=None):

    members_list = get_group_members(member_group_name)

    member_objects_list = []

    for member in members_list:

        member_type_query = GroupMember.objects.filter(member_name=member).values('member_type').distinct('member_type')

        member_types = []

        for member_type_object in member_type_query:

            member_types.append(member_type_object["member_type"])

        member_groups = get_member_groups(member)

        member_objects_list.append(Member(member_name=member,member_type=member_types,member_group_names=member_groups))


    return member_objects_list

        

    



def get_groups():

    group_list = []

    for group_object in  GroupMember.objects.distinct('member_group_name').values('member_group_name'):

        if ( group_object['member_group_name'] is not u'' ) and ( group_object['member_group_name'] is not '' ):

            group_list.append(Group(member_group_name = group_object['member_group_name'],
                                 members = get_group_members(group_object['member_group_name'])))

    return group_list


def get_members():

    member_list = []

    for member_object in  GroupMember.objects.distinct('member_name').values('member_name','member_type'):

        if ( member_object['member_name'] is not u'' ) and ( member_object['member_name'] is not '' ):


            member_list.append(Member(member_name = member_object['member_name'],
                                      member_type = member_object['member_type'],
                                      member_group_names = get_member_groups(member_object['member_name'])))


    return member_list

   


def get_member(member_name=None): 

    member_type_query = GroupMember.objects.filter(member_name=member_name).values('member_type').distinct('member_type')

    member_types = []

    for member_type_object in member_type_query:

        member_types.append(member_type_object["member_type"])

    member_groups = get_member_groups(member_name)

    return Member(member_name=member_name,member_type=member_types,member_group_names=member_groups)
