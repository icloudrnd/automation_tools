from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.groups import dashboard

class Instances(horizon.Panel):
    name = _("Groups")
    slug = "instances"


dashboard.Groups.register(Instances)
