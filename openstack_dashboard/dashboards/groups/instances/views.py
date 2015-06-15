from horizon import views
from horizon import tables
from horizon import forms
from horizon import exceptions
from horizon import tabs
import forms as project_forms
from openstack_dashboard.dashboards.groups.instances.tables import GroupsTable,MembersTable
from openstack_dashboard.api.salt_database_api import get_groups , get_members , get_member  ,  get_member_groups , get_group_members , get_group_members_wrap
#
#
from django.utils.translation import ugettext_lazy as _
from horizon.utils import memoized
#
#
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
import tabs as self_tabs




class IndexView(tabs.TabbedTableView):

    template_name = 'groups/instances/index.html'

    tab_group_class = self_tabs.GroupsAndMembers



class DetailGroupView(tables.DataTableView):

    template_name = 'groups/instances/group_detail.html'

    table_class = MembersTable

    group_name = None

    members_list = []

    def get_data(self):

        try:

            group_name = self.kwargs['group_name']

            members_list = get_group_members_wrap(group_name)

            full_url=self.request.get_full_path()

            group_verbose_name=full_url.split('/')[-1:][0]

            self.page_title = '%s members list'%(group_verbose_name)


        except Exception:
            redirect = self.get_redirect_url()
            exceptions.handle(self.request,
                              _('Unable to retrieve group details'),
                              redirect=redirect)
        return members_list

    def get_redirect_url(self):

        return reverse('horizon:groups:instances:index')


class CreateGroupView(forms.ModalFormView):
    template_name = 'groups/instances/create_group.html'
    modal_header = _("Create Group")
    form_id = "create_group_form"
    form_class = project_forms.CreateGroupForm
    submit_label = _("Create Group")
    submit_url = reverse_lazy("horizon:groups:instances:create_group")
    success_url = reverse_lazy('horizon:groups:instances:index')
    page_title = _("Create Group")



class UpdateMemberView(forms.ModalFormView):

    template_name = 'groups/instances/create_group.html'
    modal_header = _("Update Member")
    form_id = "update_member_form"
    form_class = project_forms.UpdateMemberForm
    submit_label = _("Update Member")
    submit_url = "horizon:groups:instances:update_member"
    success_url = reverse_lazy('horizon:groups:instances:index')
    page_title = _("Update Member")

    def dispatch(self, *args, **kwargs):

        return super(UpdateMemberView, self).dispatch(*args, **kwargs)

    def get_object(self):

        try:

            return get_member(self.kwargs.get('member_name',None))

        except Exception:

            redirect = reverse_lazy("horizon:groups:instances:index")
            exceptions.handle(self.request,_('Unable to retrieve member information. '),redirect=redirect)

    def get_context_data(self, **kwargs):

        context = super(UpdateMemberView, self).get_context_data(**kwargs)

        member = self.get_data()

        #table = project_forms.UpdateMemberForm(self.request)

        context["member_name"] = member
        args = (self.kwargs['member_name'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        context['modal_header'] = _("Update member "+self.kwargs['member_name'])

        return context

    def get_data(self):

        try:

            return self.get_object()

        except Exception:

            redirect = self.get_redirect_url()

            exceptions.handle(self.request,
                              _('Unable to retrieve task details.'),
                              redirect=redirect)

    def get_initial(self):

        member = self.get_object()
        member_groups = getattr(member, "member_group_names", None)
        member_types = getattr(member, "member_type", None)


        return  {'id': member.id,
                'membergroups': member_groups,
                'member_types': member_types }


    def get_redirect_url(self):

        return 'horizon:groups:instances:index'


class AddMemberView(forms.ModalFormView):
    template_name = 'groups/instances/add_member.html'
    modal_header = _("Add Member")
    form_id = "add_member_form"
    form_class = project_forms.AddMemberForm
    submit_label = _("Add Member")
    submit_url = reverse_lazy("horizon:groups:instances:add_member")
    success_url = reverse_lazy('horizon:groups:instances:index')
    page_title = _("Add Member")


class AddMemberToGroupView(forms.ModalFormView):
    template_name = 'groups/instances/add_member.html'
    modal_header = _("Add Member")
    form_id = "add_member_to_group_form"
    form_class = project_forms.AddMemberToGroupForm
    submit_label = _("Add Member")
    submit_url = "horizon:groups:instances:add_member_to_group"
    success_url = reverse_lazy("horizon:groups:instances:index")
    page_title = _("Add Member")

    def get_success_url(self): 


        url = "horizon:groups:instances:group_details"
        args = (self.kwargs['group_name'],)
        return reverse(url, args=args)

    def dispatch(self, *args, **kwargs):

        return super(AddMemberToGroupView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(AddMemberToGroupView, self).get_context_data(**kwargs)

        context['group_name'] =self.kwargs['group_name']

        args = (self.kwargs['group_name'],)
 
        context['submit_url'] = reverse(self.submit_url, args=args)
        #context['success_url'] = reverse(self.success_url, args=args)
       

        return context

    def get_initial(self):

        group_name=self.get_context_data().get('group_name',None)
        return  {'group_name': group_name}

