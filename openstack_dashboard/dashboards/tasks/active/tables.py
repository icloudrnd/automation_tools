from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables,exceptions

#
# actions

from openstack_dashboard.api.salt_api import delete_task


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, post_id):
        pass

class DeleteTasksAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Kill job",
            u"Kill jobs",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Killed job",
            u"Killed jobs",
            count
        )
    def delete(self, request, obj_id):

        try:

            delete_task(jid=obj_id)

        except exceptions.NotAvailable:

            exceptions.handle(self.request, _('Unable to delete task %s'%(str(obj_id))))


class TasksFilterAction(tables.FilterAction):
    name = "task_filter"

class ActiveTasksTable(tables.DataTable):
    id = tables.Column("id",  verbose_name = _("Id"))
    function = tables.Column("function", verbose_name = _("Function"))
    user = tables.Column("user", verbose_name = _("User"))
    target_type = tables.Column("target_type", verbose_name = _("Target Type"))
    returned = tables.Column("returned", verbose_name = _("Returned"))
    running_on = tables.Column("running_on", verbose_name = _("Running On"))
    arguments = tables.Column("arguments", verbose_name = _("Arguments"))

    class Meta:
        name = "active_tasks"
        verbose_name = _("Active Tasks")
        row_class = UpdateRow
        table_actions = (DeleteTasksAction,TasksFilterAction)
        row_actions = (DeleteTasksAction,)

