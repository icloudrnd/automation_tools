from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.tasks import dashboard

class History(horizon.Panel):
    name = _("History")
    slug = "history"


dashboard.Tasks.register(History)
