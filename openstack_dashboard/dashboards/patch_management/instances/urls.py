from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.patch_management.instances.views \
    import IndexView,PackagesToUpgradeView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'upgrade_packages/(?P<instance_id>[^/]+)$', PackagesToUpgradeView.as_view(), name='upgrade_packages'),
)
