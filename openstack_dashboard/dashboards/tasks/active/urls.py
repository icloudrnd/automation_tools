from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.tasks.active.views \
    import IndexView # ScopeView,ArgumentsView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^$', IndexView.as_view(), name='scope'),
)
