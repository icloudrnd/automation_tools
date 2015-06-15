from horizon import views
from horizon import exceptions
from horizon import tabs
from tables import InstanceTable,PackagesForUpgradeTable
from horizon import tables, exceptions

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


from openstack_dashboard.api.salt_api import minions_list_custom,pkg_list_for_upgrade

class IndexView(tables.DataTableView):
    # A very simple class-based view...

    template_name = 'patch_management/instances/index.html'
    table_class = InstanceTable

    def get_data(self):
        # Add data to the context here...

        minions = []

        try:

            minions = minions_list_custom()

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))
             
        return minions


class PackagesToUpgradeView(tables.DataTableView):
    template_name = 'patch_management/instances/packages_index.html'

    table_class = PackagesForUpgradeTable

    instance_name = None

    def get_data(self):
        print '-->>'
        
        print dir(self.table)
        print '-->>'
        # test: my fresh view
        pkgs_list = []

        try:

            instance_id = self.kwargs['instance_id']

            pkgs_list = pkg_list_for_upgrade(instance_name=instance_id)

            self.table.instance_name = instance_id
            #
            # test
            #
            full_url=self.request.get_full_path()
            #
            instance_name=full_url.split('/')[-1:][0]
            #
            self.page_title = 'Packages available to upgrade on %s'%(instance_name)

            print self.page_title

            print '-->>'

            print dir(self.table)

            print '-->>'
            
        except Exception:
            redirect = self.get_redirect_url()
            exceptions.handle(self.request,
                              _('Unable to retrieve packages to upgrade'),
                              redirect=redirect)
        return pkgs_list

    def get_redirect_url(self):

        return ('patch_management/upgrade_packages/%s'%(self.instance_name))


