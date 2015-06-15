from horizon import views
from horizon import exceptions
from tables import ActiveTasksTable
from horizon import tables, exceptions
from django.utils.translation import ugettext_lazy as _


from openstack_dashboard.api.salt_api import active_jobs

class IndexView(tables.DataTableView):
    # A very simple class-based view...

    template_name = 'tasks/active/index.html'
    table_class = ActiveTasksTable

    def get_data(self):
        # Add data to the context here...

        active_jobs_list = []

        try:

            active_jobs_list = active_jobs()

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))
             
        return active_jobs_list

class ScopeView(views.HorizonTemplateView):

    pass

class ArgumentsView(views.HorizonTemplateView):

    pass
