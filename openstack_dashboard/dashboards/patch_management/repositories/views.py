from horizon import views
from horizon import exceptions
from horizon import tabs
from tabs import RpmAndDevTabs
from horizon import tables, exceptions, forms

from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from openstack_dashboard.api.salt_api import get_repo_list_rpm,get_repo_list_deb
from openstack_dashboard.api.salt_database_api import get_groups


from horizon import workflows
import workflows as self_workflows
import forms as self_forms

from tables import YumRepositoriesTable,ZypperRepositoriesTable


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

class SelectGrainView(forms.ModalFormView):

    print 'select grain class'

    form_class = self_forms.SelectGrain
    form_id = "select_grain"
    modal_header = _("Select Grain")
    template_name = 'patch_management/repositories/select_grain.html'
    submit_label = _("Add")

    submit_url = reverse_lazy(
        "horizon:patch_management:repositories:select_grain")

    success_url = reverse_lazy('horizon:patch_management:repositories:index')

    page_title = _("Select Grain")

