from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.patch_management import dashboard



class Instances(horizon.Panel):
    name = _("Instances")
    slug = "instances"


dashboard.PatchManagement.register(Instances)
