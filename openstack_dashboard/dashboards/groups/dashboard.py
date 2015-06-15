from django.utils.translation import ugettext_lazy as _

import horizon


class GroupsPanelGroup(horizon.PanelGroup):
    slug = "tasks_panel_group"
    #name = _("")
    panels = ('instances',)


class Groups(horizon.Dashboard):
    name = _("Group Management")
    slug = "groups"
    panels = (GroupsPanelGroup,)  # Add your panels here.
    default_panel = 'instances'  # Specify the slug of the dashboard's default panel.


horizon.register(Groups)
