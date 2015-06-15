from horizon import views
from horizon import tables
from openstack_dashboard.dashboards.tasks.completed.tables import CompletedTasksTable
from openstack_dashboard.api.salt_database_api import get_all_records,task_body_harp,get_all_records_mod
#
#
from django.utils.translation import ugettext_lazy as _
from horizon.utils import memoized
#
#
from django.core.urlresolvers import reverse
from horizon import exceptions



class IndexView(tables.DataTableView):
    # A very simple class-based view...

    template_name = 'tasks/completed/index.html'
    table_class = CompletedTasksTable

    def has_more_data(self, table):

        return self._more


    def get_data(self):
        # Add data to the context here...

        completed_jobs_list = []

        self._more = False

        marker = self.request.GET.get(CompletedTasksTable._meta.pagination_param, None)

        try:

            completed_jobs_list , self._more  = get_all_records_mod(self.request,paginate=True,marker=marker)

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Database connection is not available'))

            

        return completed_jobs_list

class DetailView(views.HorizonTemplateView):
    template_name = 'tasks/completed/detail.html'
    page_title = _("Task Details: {{ task.id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        task = self.get_data()
        table = CompletedTasksTable(self.request)

        context["task"] = task
        return context


    @memoized.memoized_method
    def get_data(self):
        try:
            task_id = self.kwargs['task_id']
            task = task_body_harp(job_id=task_id)
        except Exception:
            redirect = self.get_redirect_url()
            exceptions.handle(self.request,
                              _('Unable to retrieve task details.'),
                              redirect=redirect)
        return task

    def get_redirect_url(self):
        return reverse('horizon:tasks:completed:index')





