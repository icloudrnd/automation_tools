from django.utils.translation import ugettext_lazy as _
#from openstack_dashboard.api.salt_api import gen_history_report

from horizon import tables

class DownloadHistory(tables.LinkAction):
    name = "events_history"
    verbose_name = _("Download events history")
    icon = "download"

    def get_link_url(self,usage=None):
        #return self.table.kwargs['usage'].csv_link()


        #return gen_history_report(self.table.kwargs['id'])
        pass



class InstancesTable(tables.DataTable):
    id = tables.Column("id",  verbose_name = _("Instance"))
    function = tables.Column("function", verbose_name = _("Last executed function"))
    added = tables.Column("added", verbose_name = _("Added"))
    success = tables.Column("success", verbose_name = _("Success"))
    active_tasks = tables.Column("active_tasks", verbose_name = _("Active Tasks"))

    class Meta:
        name = "tasks_history"
        verbose_name = _("Tasks History")
        row_actions = (DownloadHistory,)

class InstancesFilterAction(tables.FilterAction):
    name = "instances_filter"
