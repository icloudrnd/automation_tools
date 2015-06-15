from django.utils.translation import ugettext_lazy as _
#
from collections import defaultdict

from horizon import tables,exceptions
#
from openstack_dashboard.api.salt_database_api import  event_types

class FunFilter(tables.FixedFilterAction):
    def get_fixed_buttons(self):



        def make_dict(text, fun, icon):
            return dict(text=text, value=fun, icon=icon)

        

        buttons = [make_dict(_('all'), 'all', '')]
 
        fun_list = []

        fun_list = event_types() 

        for fun_name in fun_list:

            buttons.append(make_dict(_(str(fun_name)), str(fun_name.replace('.','-')), ''))

        return buttons

    def categorize(self, table, db_task_entries):

        functions = defaultdict(list)

        for entry in db_task_entries:

            functions[(entry.function).replace('.','-')].append(entry.id)

            functions['all'].append(entry.id)


        return functions


class UpdateRow(tables.Row):

    ajax = True

    def get_data(self, request, post_id):
        pass

    def load_cells(self, task=None):

        super(UpdateRow, self).load_cells(task)

        task = self.datum

        fun_categories = ['all']

        fun_categories.append(str(task.function))

        for category in fun_categories:
            
            self.classes.append('category-' + category.replace('.','-'))




class TasksFilterAction(tables.FilterAction):
    #  two filters are not available

    name = "task_filter"

class CompletedTasksTable(tables.DataTable):
    id = tables.Column("id",  verbose_name = _("Id"), link="horizon:tasks:completed:detail")
    function = tables.Column("function",  verbose_name = _("Function"))
    added = tables.Column("added", verbose_name = _("Added"))

    class Meta:
        name = "completed_tasks"
        verbose_name = _("Completed Tasks")
        table_actions = (FunFilter,)
        row_class = UpdateRow
        pagination_param = "jid_marker"

    




class TasksFilterAction(tables.FilterAction):
    name = "task_filter"

class TaskDetailsFilterAction(tables.FilterAction):
    name = "task_details_filter"
