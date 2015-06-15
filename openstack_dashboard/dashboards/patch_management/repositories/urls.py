from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.patch_management.repositories.views \
    import IndexView,CreateRepositoryView,SelectGrainView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create$', CreateRepositoryView.as_view(), name='create'),
    url(r'^select_grain$', SelectGrainView.as_view(), name='select_grain'),
    
)
