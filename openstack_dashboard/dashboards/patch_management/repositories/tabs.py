from horizon import tabs
from horizon import exceptions
from django.utils.translation import ugettext_lazy as _

from tables import YumRepositoriesTable,ZypperRepositoriesTable,DebRepositoriesTable

from openstack_dashboard.api.salt_api import get_repo_list_rpm,get_repo_list_deb

class RpmTab(tabs.TableTab):
    table_classes = (YumRepositoriesTable,ZypperRepositoriesTable)
    name = _("Rpm")
    slug = "rpm_tab"
    template_name = ("patch_management/repositories/yum_rpm_table.html")
    #template_name = ("horizon/common/_detail_table.html")
    preload = True

    def get_yumrepositories_data(self):

        repositories = []

        try:

            repositories = get_repo_list_rpm("yum")

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))

        return repositories

    def get_zypperrepositories_data(self):

        repositories = []

        try:

            repositories = get_repo_list_rpm("zypper")

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))

        return repositories



class DebTab(tabs.TableTab):
    table_classes = (DebRepositoriesTable,)
    name = _("Deb")
    slug = "dev_tab"
    template_name = ("horizon/common/_detail_table.html")
    preload = True

    def get_debrepositories_data(self):

        repositories = []

        try:

            repositories = get_repo_list_deb()

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))

        return repositories



class RpmAndDevTabs(tabs.TabGroup):
    slug = "rpm_and_deb"
    tabs = (RpmTab, DebTab)
    sticky = True

