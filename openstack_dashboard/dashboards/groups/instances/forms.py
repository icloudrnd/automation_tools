from horizon import forms
from horizon import exceptions
from horizon import messages

#
#from openstack_dashboard.api.salt_database_api import create_member_group , create_member ,  get_groups , get_members , get_group_members , update_member , get_member

from openstack_dashboard.api.salt_sls_api import create_group_sls as  create_member_group
from openstack_dashboard.api.salt_sls_api import get_groups_sls as  get_groups
from openstack_dashboard.api.salt_sls_api import get_members_sls_custom  as get_members
from openstack_dashboard.api.salt_sls_api import get_member_sls as get_member
from openstack_dashboard.api.salt_sls_api import get_group_members_sls as get_group_members_wrap
from openstack_dashboard.api.salt_sls_api import update_member_sls as update_member
from openstack_dashboard.api.salt_sls_api import get_group_members_simple_sls as get_group_members




from openstack_dashboard.api.salt_api import minions_list
from django.utils.translation import ugettext_lazy as _




class CreateGroupForm(forms.SelfHandlingForm):

    id = forms.CharField(label=_("New Group Name:"), max_length=255)

    def __init__(self, request, *args, **kwargs):

        super(CreateGroupForm, self).__init__(request, *args, **kwargs)


    def handle(self, request, data):

        new_group_name = data.pop('id')

        try:

            create_member_group(new_group_name)

            messages.success(request, _('Group %s  has been created successfully.'%(new_group_name)))

            return True

        except exceptions.Conflict:

            msg = _('Group "%s" is already exist.' % new_group_name)

            messages.error(request, msg)

            return False

        except Exception:

            response = exceptions.handle(request, ignore=True)

            messages.error(request, _('Unable to create the group.'))


class UpdateMemberForm(forms.SelfHandlingForm):

    id = forms.CharField(label=_("Member Name"), widget=forms.HiddenInput)

    member_types = forms.CharField(max_length=255, label=_("Member Type") ,  widget=forms.HiddenInput)

    membergroups = forms.MultipleChoiceField(label=_("Member Groups"),widget=forms.CheckboxSelectMultiple(),required = False)

    def __init__(self, request, *args, **kwargs):

        super(UpdateMemberForm, self).__init__(request, *args, **kwargs)

        initial_group_names = self.initial.get('membergroups',None)

        member_groups_tuple = []

        if initial_group_names:

            member_groups_tuple = [(group_name, group_name) for group_name in initial_group_names ]

            for group in get_groups():
 
                if group.id not in initial_group_names:

                    member_groups_tuple.append((str(group.id),str(group.id)))

            self.fields['membergroups'].choices = member_groups_tuple

        else:

            for group in get_groups():

                member_groups_tuple.append((str(group.id),str(group.id)))

            self.fields['membergroups'].choices = member_groups_tuple




    def handle(self, request, data):

        print '<< update_member handle'

        try:


            member_name=data['id']
            member_groups=data['membergroups']
            member_type=data['member_types']
            result = update_member(member_name=member_name,member_type=member_type,member_group_names=member_groups)
      
            print "====" 
            print result
            print "===="
        
            return True


        except Exception:

            response = exceptions.handle(request, ignore=True)

            messages.error(request, _('Unable to update member'))

class AddMemberForm(forms.SelfHandlingForm):


    group_name = forms.CharField(label=_("Group Name"), widget=forms.HiddenInput ,  required = False)
    salt_minions = forms.MultipleChoiceField(label=_("Salt Minions"),widget=forms.CheckboxSelectMultiple(),required = True)


    def __init__(self, request, *args, **kwargs):

        super(AddMemberForm, self).__init__(request, *args, **kwargs)

        #initial_salt_minions_list = self.initial.get('minions_list',None)

        minions_list_tuple = []

        registered_members = []
        registered_members_objects = get_members()

        for member in registered_members_objects:

            registered_members.append(member.id)

        for minion in minions_list():

            if minion not in registered_members:

                minions_list_tuple.append((str(minion),str(minion)))

        self.fields['salt_minions'].choices = minions_list_tuple




    def handle(self, request, data):

        try:

            minions_list =  data.get('salt_minions',None)

            registered_members = []
            registered_members_objects = get_members()

            for member in registered_members_objects:

                registered_members.append(member.id) 

            if minions_list:


                for minion in minions_list:

                    if minion not in registered_members:

                        pass
                        #create_member(member_name=minion,member_type="instance",member_group_names=[])
            

            return True



        except Exception:

            response = exceptions.handle(request, ignore=True)

            messages.error(request, _('Unable to update member'))

class AddMemberToGroupForm(forms.SelfHandlingForm):


    group_name = forms.CharField(label=_("Group Name"), widget=forms.HiddenInput ,  required = False)
    members = forms.MultipleChoiceField(label=_("Existing Members"),widget=forms.CheckboxSelectMultiple(),required = True)


    def __init__(self, request, *args, **kwargs):

        super(AddMemberToGroupForm, self).__init__(request, *args, **kwargs)

        group_name = self.initial.get('group_name',None)

        members_list_tuple = []

        available_members = []

        available_members_tuple = []

        existing_group_members = get_group_members(group_name)

        for member in get_members():

            if member.id not in existing_group_members:
   
                available_members.append(member.id)

        for member in available_members:

            available_members_tuple.append((str(member),str(member)))

        self.fields['members'].choices = available_members_tuple 




    def handle(self, request, data):

        try:

            selected_members =  data.get('members',None)
            group_name = data.get('group_name',None)

            
            for member in selected_members:

                member_info = get_member(member)

                current_member_groups = member_info.member_group_names

                current_member_groups.append(group_name)
                
                update_member(member_name=member,member_type=str(member_info.member_type),member_group_names=current_member_groups)


            return True



        except Exception:

            response = exceptions.handle(request, ignore=True)

            messages.error(request, _('Unable to update member'))

