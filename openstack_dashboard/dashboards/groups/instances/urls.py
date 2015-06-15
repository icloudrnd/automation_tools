from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.groups.instances.views import IndexView,DetailGroupView,CreateGroupView,UpdateMemberView,AddMemberView,AddMemberToGroupView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'(?P<group_name>[^/]+)/group_details/$', DetailGroupView.as_view(), name='group_details'), 
    url(r'^create_group/$', CreateGroupView.as_view(), name='create_group'),
    url(r'^add_member/$', AddMemberView.as_view(), name='add_member'),
    url(r'^(?P<group_name>[^/]+)/add_member/$', AddMemberToGroupView.as_view(), name='add_member_to_group'),
    url(r'^(?P<member_name>[^/]+)/update_member/$', UpdateMemberView.as_view(), name='update_member'),

)
