from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.patch_management import dashboard



class Repositories(horizon.Panel):
    name = _("Repositories")
    slug = "repositories"


dashboard.PatchManagement.register(Repositories)
