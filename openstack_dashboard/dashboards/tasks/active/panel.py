from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.tasks import dashboard



class Active(horizon.Panel):
    name = _("Active")
    slug = "active"


dashboard.Tasks.register(Active)
