from horizon import workflows
from horizon import forms
from horizon.forms import fields
from horizon import exceptions

from django.utils.translation import ugettext_lazy as _

from django.views.decorators.debug import sensitive_variables

from openstack_dashboard.api.salt_database_api import get_groups , get_group_members
from openstack_dashboard.api.salt_api import add_yum_repo , add_zypper_repo 


class ModifyYumRepositoryAction(workflows.Action):

    repo = forms.CharField(label=_("Repository"),
                           max_length=255,
                           required=True)

    name = forms.CharField(label=_("Repository Name"),
                           max_length=255,
                           required=True)

    baseurl = forms.CharField(label=_("Baseurl"),
                           max_length=4096,
                           required=True)

    mirrorlist = forms.CharField(label=_("Mirrorlist"),
                           max_length=4096,
                           required=True)

    gpgkey = forms.CharField(label=_("gpgkey"),
                           max_length=4096)

    failovermethod = forms.ChoiceField(label=_("Failover method"))

    file = forms.CharField(label=_("file"),
                           max_length=4096)

    enabled = forms.BooleanField(label=_("Enabled"),
                                             required=False,
                                             help_text=_("enable or disable (True or False) repository, but do not remove if disabled."))

    refresh = forms.BooleanField(label=_("Refresh"),
                                             required=False,
                                             help_text=_("enable or disable (True or False) auto-refresh of the repository."))

    cache = forms.BooleanField(label=_("Cache"),
                                             required=False,
                                             help_text=_("Enable or disable (True or False) RPM files caching."))

    gpgcheck = forms.BooleanField(label=_("gpgcheck"),
                                             required=False,
                                             help_text=_("Enable or disable (True or False) GOG check for this repository."))

    skip_if_unavailable = forms.BooleanField(label=_("Skip if unavailable"),
                                             required=False,
                                             help_text=_("Automatically trust and import new repository."))




    def __init__(self, request, context, *args, **kwargs):

        super(ModifyYumRepositoryAction, self).__init__(request, context, *args, **kwargs)

        failover_methods = [(method, method) for method in ["None","priority","roundRobin"]]

        self.fields['failovermethod'].choices = failover_methods

    class Meta(object):

        name = _("Modify Yum Repo")

class ModifyZypperRepositoryAction(workflows.Action):

    repo = forms.CharField(label=_("Repository"),
                           max_length=255,required=True)

    name = forms.CharField(label=_("Repository Name"),
                           max_length=255)

    alias = forms.CharField(label=_("Alias"),
                           max_length=255)

    baseurl = forms.CharField(label=_("Baseurl"),
                           max_length=4096,
                           required=True)

    mirrorlist = forms.CharField(label=_("Mirrorlist"),
                           max_length=4096)

    url = forms.CharField(label=_("Url"),
                           max_length=4096)

    packagesPath = forms.CharField(label=_("Packages Path"),
                           max_length=4096)

    metadataPath = forms.CharField(label=_("Metadata Path"),
                           max_length=4096)

    mirrorlist = forms.CharField(label=_("Mirrorlist"),
                           max_length=4096)

    repo_type = forms.CharField(label=_("Type"),
                           max_length=4096)

    enabled = forms.BooleanField(label=_("enabled"),
                                             required=True,
                                             help_text=_("enable or disable (True or False) repository, but do not remove if disabled."))

    refresh = forms.BooleanField(label=_("refresh"),
                                             required=True,
                                             help_text=_("enable or disable (True or False) auto-refresh of the repository."))

    cache = forms.BooleanField(label=_("cache"),
                                             required=True,
                                             help_text=_("Enable or disable (True or False) RPM files caching."))

    gpgcheck = forms.BooleanField(label=_("gpgcheck"),
                                             required=True,
                                             help_text=_("Enable or disable (True or False) GOG check for this repository."))

    gpgautoimport = forms.BooleanField(label=_("gpgautoimport"),
                                             required=True,
                                             help_text=_("Automatically trust and import new repository."))

    keeppackages = forms.BooleanField(label=_("keeppackages"),
                                             required=False,
                                             help_text=_("Automatically trust and import new repository."))


    def __init__(self, request, context, *args, **kwargs):

        super(ModifyZypperRepositoryAction, self).__init__(request, context, *args, **kwargs)


    class Meta(object):

        name = _("Modify Zypper Repo")




class SetYumRepositoryChoice(workflows.Step):

    action_class = ModifyYumRepositoryAction

    template_name = "patch_management/repositories/_details.html"

    def contribute(self, data, context):

        context['repo']=data.get("repo","")
        context['name']=data.get("name","")
        context['baseurl']=data.get("baseurl","")
        context['mirrorlist']=data.get("mirrorlist","")
        context['gpgkey']=data.get("gpgkey","")
        context['failovermethod']=data.get("failovermethod","")     
        context['file']=data.get("file","")
        context['enabled']=data.get("enabled","") 
        context['refresh']=data.get("refresh","")
        context['cache']=data.get("cache","")
        context['gpgcheck']=data.get("gpgcheck","")
        context['skip_if_unavailable']=data.get("skip_if_unavailable","")
        
        
        

        return context
        

class SetZypperRepositoryChoice(workflows.Step):

    action_class = ModifyZypperRepositoryAction

    template_name = "patch_management/repositories/_details.html"

    def contribute(self, data, context):

        context['repo']=data.get("repo","")
        context['baseurl']=data.get("baseurl","")
        context['enabled']=data.get("enabled","")
        context['refresh']=data.get("refresh","")
        context['cache']=data.get("cache","")
        context['gpgcheck']=data.get("gpgcheck","")
        context['gpgautoimport']=data.get("gpgautoimport","")
        context['repository_type']=data.get("repository_type","")
 
        return context


    


class CreateYumRepository(workflows.Workflow):

    slug = "create_repository"

    name = _("Create Repository")

    finalize_button_name = _("Create")

    success_message = _('Scheduled repository creating "%s".')

    failure_message = _('Unable to create repository "%s".')

    success_url = "horizon:patch_management:repositories:index"

    default_steps = (SetRepositoryChoice,SetScopeForNewRpmRepositoryChoice)

    @sensitive_variables('context')
    def handle(self, request, context):

        try:

            repo=context.get("repo","")
            name=context.get("name","")
            baseurl=context.get("baseurl","")
            mirrorlist=context.get("mirrorlist","")

            target_groups = context.get("group_multiselect","")
            target_members = []

            for group in target_groups:

                group_members = get_group_members(group)

                for member in group_members:

                    #   add_yum_repo
                    add_yum_repo(instance_name = member, repo = repo , name = name , baseurl = baseurl , mirrorlist = mirrorlist)
                 
            return True
            

        except Exception:

            exceptions.handle(request)

            return False



class CreateZypperRepository(workflows.Workflow):

    slug = "create_repository"

    name = _("Create Repository")

    finalize_button_name = _("Create")

    success_message = _('Scheduled repository creating "%s".')

    failure_message = _('Unable to create repository "%s".')

    success_url = "horizon:patch_management:repositories:index"

    default_steps = (SetRepositoryChoice,SetScopeForNewRpmRepositoryChoice)

    @sensitive_variables('context')
    def handle(self, request, context):

        try:

            repo=context.get("repo","")
            baseurl=context.get("baseurl","")
            enabled=context.get("enabled","")
            refresh=context.get("refresh","")
            cache=context.get("cache","")
            gpgcheck=context.get("gpgcheck","")
            gpgautoimport=context.get("gpgautoimport","")
            repository_type=context.get("repository_type","")

            target_groups = context.get("group_multiselect","")
            target_members = []

            for group in target_groups:

                group_members = get_group_members(group)

                for member in group_members:

                    if member not in target_members:

                        target_members.append(member)


            for tmember in target_members:


                add_zypper_repo(instance_name=tmember,
                                    repo=repo,
                                    baseurl=baseurl,
                                    enabled=enabled,
                                    refresh=refresh,
                                    cache=cache,
                                    gpgcheck=gpgcheck,
                                    gpgautoimport=gpgautoimport)




            return True

        except Exception:

            exceptions.handle(request)

            return False

