from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.tasks import dashboard

class Completed(horizon.Panel):
    name = _("Completed")
    slug = "completed"


dashboard.Tasks.register(Completed)
