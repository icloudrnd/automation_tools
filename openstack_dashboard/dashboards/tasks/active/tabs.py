from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.tasks import tables

class TasksTab(tabs.TableTab)

    name = _("Tasks Tab")
    slug = "tasks_tab"
    table_classes = (tables.TasksTable)
    template_name = ("horizon/common/_detail_table.html")
    preload = False
    
    def has_more_data(self, table):
        return self._has_more

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(tables.InstanceTable._meta)
class ActiveTaskOverviewTab(tabs.Tab):
    name = _("Task Overview")
    slug = "active_task_overview"
    #template_name = ("project/volumes/volumes/_detail_overview.html")

    def get_context_data(self, request):
        pass
        #return {"volume": self.tab_group.kwargs['volume']}

