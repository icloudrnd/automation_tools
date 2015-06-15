from django.utils.translation import ugettext_lazy as _

import horizon


class PatchManagementPanelGroup(horizon.PanelGroup):
    slug = "patch_management_panel_group"
    #name = _("")
    panels = ('instances','repositories')


class PatchManagement(horizon.Dashboard):
    name = _("Patch Management")
    slug = "patch_management"
    panels = (PatchManagementPanelGroup,)  # Add your panels here.
    default_panel = 'instances'  # Specify the slug of the dashboard's default panel.


horizon.register(PatchManagement)
