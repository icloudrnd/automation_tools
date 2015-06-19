from horizon import views
from horizon import exceptions
from horizon import tabs
from openstack_dashboard.dashboards.patch_management.repositories.tabs import RpmAndDevTabs
from horizon import tables, exceptions, forms

from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from openstack_dashboard.api.salt_api import get_repo_list_rpm,get_repo_list_deb
from openstack_dashboard.api.salt_database_api import get_groups


from horizon import workflows
import workflows as self_workflows
import forms as self_forms

from tables import YumRepositoriesTable,ZypperRepositoriesTable,RepositoryMembersTable


class IndexView(tabs.TabbedTableView):


    #table_classes = (YumRepositoriesTable,ZypperRepositoriesTable)
    template_name = 'patch_management/repositories/index.html'
    tab_group_class = RpmAndDevTabs

class CreateRepositoryView(workflows.WorkflowView):


    workflow_class = self_workflows.CreateRpmRepository

    #def get_initial(self):
        #initial = super(CreateRepositoryView, self).get_initial()
        #package_manager_name = self.request.GET.get(CompletedTasksTable._meta.package_manager_name, None)
        #initial['repository_type'] = package_manager_name
        #return initial

class RepositoryMembersView(tables.DataTableView):

    table_class = RepositoryMembersTable
    template_name = 'patch_management/repositories/repo_detail.html'

    def get_data(self):

        print  ":: Self ::"
        print self
        print dir(self)
     
        print "==========="
        print self.table.kwargs.get('instances',None)
        print "==========="
        print "self.table"
        print self.table
        print dir(self.table)
        print "---------"

class SelectGrainView(forms.ModalFormView):

    form_class = self_forms.SelectGrain
    form_id = "select_grain"
    modal_header = _("Select Grain")
    template_name = 'patch_management/repositories/select_grain.html'
    submit_label = _("Add")

    submit_url = reverse_lazy(
        "horizon:patch_management:repositories:select_grain")

    success_url = reverse_lazy('horizon:patch_management:repositories:index')

    page_title = _("Select Grain")

