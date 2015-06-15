from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.tasks.completed.views import IndexView,DetailView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<task_id>[^/]+)/detail/$', DetailView.as_view(), name='detail'), 
)
