from django.utils.translation import ugettext_lazy as _

import horizon


class TasksPanelGroup(horizon.PanelGroup):
    slug = "tasks_panel_group"
    #name = _("")
    panels = ('active','completed','history',)


class Tasks(horizon.Dashboard):
    name = _("Tasks")
    slug = "tasks"
    panels = (TasksPanelGroup,)  # Add your panels here.
    default_panel = 'active'  # Specify the slug of the dashboard's default panel.


horizon.register(Tasks)
