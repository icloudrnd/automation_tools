from horizon import tabs
from django.utils.translation import ugettext_lazy as _

from tables import GroupsTable,MembersTable

from openstack_dashboard.api.salt_database_api import get_members, get_groups 

class GroupsTab(tabs.TableTab):
    table_classes = (GroupsTable,)
    name = _("Groups")
    slug = "groups_tab"
    template_name = ("horizon/common/_detail_table.html")
    preload = True

    def get_groups_data(self):

        groups = []

        try:

            groups = get_groups()


        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))

        return groups



class MembersTab(tabs.TableTab):
    table_classes = (MembersTable,)
    name = _("Members")
    slug = "members_tab"
    template_name = ("horizon/common/_detail_table.html")
    preload = True

    def get_members_data(self):

        members = []

        try:

            members = get_members()

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))

        return members



class GroupsAndMembers(tabs.TabGroup):
    slug = "groups_and_members"
    tabs = (GroupsTab, MembersTab)
    sticky = True
