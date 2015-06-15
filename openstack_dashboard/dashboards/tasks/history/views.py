from horizon import views,tables
from tables import InstancesTable
from openstack_dashboard.api.salt_database_api import fill_history



class IndexView(tables.DataTableView):
    # A very simple class-based view...

    template_name = 'tasks/history/index.html'
    table_class = InstancesTable

    def get_data(self):
        # Add data to the context here...

        instance_list = []

        try:

            instance_list = fill_history()

        except exceptions.NotAvailable:

            exceptions.handle(self.request,_('Unable to connect to Salt-master:'))

        return instance_list

