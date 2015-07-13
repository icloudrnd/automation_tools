from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django.utils import http
from django import template
#
from collections import defaultdict

from horizon import tables,exceptions
from django.core.urlresolvers import reverse
#
####from openstack_dashboard.api.salt_database_api import get_group_members_wrap, get_member ,   remove_group , remove_member, update_member
from openstack_dashboard.api.salt_sls_api import get_group_members_sls as get_group_members_wrap 
from openstack_dashboard.api.salt_sls_api import get_member_sls as get_member
from openstack_dashboard.api.salt_sls_api import del_group as remove_group
from openstack_dashboard.api.salt_sls_api import remove_everywhere as remove_member
from openstack_dashboard.api.salt_sls_api import update_member_sls as update_member



class EditMemberLink(tables.LinkAction):
    name = "edit_member"
    verbose_name = _("Edit Member")
    url = "horizon:groups:instances:update"
    classes = ("ajax-modal",)
    icon = "pencil"

class CreateGroupLink(tables.LinkAction):
    name = "create_group"
    verbose_name = _("Create Group")
    url = "horizon:groups:instances:create_group"
    classes = ("ajax-modal",)
    icon = "plus"

class AddMemberLink(tables.LinkAction):
    name = "add_member"
    verbose_name = _("Add Member")
    url = "horizon:groups:instances:add_member"
    classes = ("ajax-modal",)
    icon = "plus"
  
    def get_link_url(self, datum=None):

        group_name = self.table.kwargs.get('group_name',None)

        if group_name:

            url = "horizon:groups:instances:add_member_to_group"

            return reverse(url, args=(group_name,))

        return reverse(self.url)


class UpdateMemberLink(tables.LinkAction):
    name = "update_member"
    verbose_name = _("Update Member")
    url = "horizon:groups:instances:update_member"
    classes = ("ajax-modal",)
    icon = "pencil"


class UpdateGroupRow(tables.Row):

    ajax = True

    def get_data(self, request, group_id):
        group_info = get_group_members_wrap(group_id)
        return group_info


class UpdateMemberRow(tables.Row):

    ajax = True

    def get_data(self, request, member_id):
        member_info = get_member(member_id)
        return member_info



class DeleteGroupsAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Group",
            u"Delete Groups",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Group",
            u"Deleted Groups",
            count
        )

    def delete(self, request, obj_id):
        remove_group(obj_id)

class DeleteMembersAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Member",
            u"Delete Members",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Member",
            u"Deleted Members",
            count
        )

    def delete(self, request, obj_id):

        group_name=self.table.kwargs.get('group_name',None)

        if group_name !=None:
            member_info = get_member(obj_id) 
            current_member_groups = member_info.member_group_names
            current_member_groups.remove(group_name)
            update_member(member_name=obj_id,member_type=str(member_info.member_type),member_group_names=current_member_groups)
            return None
            
            
        remove_member(obj_id)

def get_Member_groups(instance):

    template_name = 'groups/instances/_member_groups.html' 
    member_groups = instance.member_group_names
    member_name = instance.id

    member_group_conv = []

    for group in member_groups:

       member_group_conv.append(str(group)) 

    context = {'member_name':member_name , 'member_groups':member_group_conv}

    return template.loader.render_to_string(template_name, context)

def get_Group_members(instance):

    template_name = 'groups/instances/_group_members.html'
    group_name = instance.id
    group_members = instance.members

    members_conv = []

    for member in group_members:

        members_conv.append(str(member))

    context = {'group_name':group_name , 'group_members':members_conv}

    return template.loader.render_to_string(template_name, context)






class GroupsTable(tables.DataTable):
    id = tables.Column("id",  verbose_name = _("Group Name"), link="horizon:groups:instances:group_details")
    members = tables.Column(get_Group_members,  verbose_name = _("Members"))

    class Meta:
        name = "groups"
        verbose_name = _("Groups")
        table_actions = (CreateGroupLink,DeleteGroupsAction)
        row_class = UpdateGroupRow

class MembersTable(tables.DataTable):
    id = tables.Column("id",  verbose_name = _("Member"))
    member_type = tables.Column("member_type",  verbose_name = _("Type"))
    member_group_names = tables.Column(get_Member_groups, verbose_name = _("Member Groups"))

    class Meta:
        name = "members"
        verbose_name = _("Members")
        table_actions = (DeleteMembersAction,AddMemberLink)
        row_actions = (UpdateMemberLink,)
        row_class = UpdateMemberRow







class TasksFilterAction(tables.FilterAction):
    name = "task_filter"

class TaskDetailsFilterAction(tables.FilterAction):
    name = "task_details_filter"
