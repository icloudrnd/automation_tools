from horizon import workflows
from horizon import forms
from horizon.forms import fields
from horizon import exceptions

from django.utils.translation import ugettext_lazy as _

from django.views.decorators.debug import sensitive_variables

from openstack_dashboard.api.salt_database_api import get_groups , get_group_members
from openstack_dashboard.api.salt_api import add_yum_repo , add_zypper_repo 


class SetRpmRepositoryDetailsAction(workflows.Action):

    repository_type = forms.ChoiceField(label=_("Choose repo type"),required=False)

    ###
    ### initial part required to create YUM or ZYPPER repository
    ###

    repo = forms.CharField(label=_("Repository"),
                           max_length=255)

    name = forms.CharField(label=_("Repository Name"),
                           max_length=255)

    baseurl = forms.CharField(label=_("Baseurl"),
                           max_length=4096)

    mirrorlist = forms.CharField(label=_("Mirrorlist"),
                           max_length=4096)
    ###
    ### initial part required to create ZYPPER repository
    ###

    enabled = forms.BooleanField(label=_("Enabled"),
                                             initial=True,
                                             required=False,
                                             help_text=_("enable or disable (True or False) repository, but do not remove if disabled."))

    refresh = forms.BooleanField(label=_("Refresh"),
                                             initial=True,
                                             required=False,
                                             help_text=_("enable or disable (True or False) auto-refresh of the repository."))

    cache = forms.BooleanField(label=_("Cache"),
                                             initial=True,
                                             required=False,
                                             help_text=_("Enable or disable (True or False) RPM files caching."))

    gpgcheck = forms.BooleanField(label=_("gpgcheck"),
                                             initial=True,
                                             required=False,
                                             help_text=_("Enable or disable (True or False) GOG check for this repository."))

    gpgautoimport = forms.BooleanField(label=_("gpgautoimport"),
                                             initial=True,
                                             required=False,
                                             help_text=_("Automatically trust and import new repository."))



    def __init__(self, request, context, *args, **kwargs):

        super(SetRpmRepositoryDetailsAction, self).__init__(request, context, *args, **kwargs)


        self.fields['repository_type'].choices = [('zypper','zypper'),('yum','yum')]

#    def clean(self):

#        print ">> clean >>"




    class Meta(object):

        name = _("Details")

SELECT_GRAIN_URL="horizon:patch_management:repositories:select_grain"


class MultipleChoiceFieldWithoutValidate(forms.MultipleChoiceField):

    def validate(self, value):
        pass

    

class SetScopeForNewRpmRepositoryDetailsAction(workflows.Action):


    grainpairmultiselect = MultipleChoiceFieldWithoutValidate(label=_("Available grain pairs"),
                                        widget=forms.CheckboxSelectMultiple(),
                                        required=True,
                                        error_messages={
                                            'required': _(
                                                "At least one criteria must"
                                                " be specified.")},
                                        help_text=_("Create repository"
                                                    " on instances matching those grains"))

    grainpair = forms.DynamicChoiceField(label=_("New grainpair"),
                                       required=False,
                                       add_item_link=SELECT_GRAIN_URL)

    group_multiselect = forms.MultipleChoiceField(label=_("Available member groups"),
                                        widget=forms.CheckboxSelectMultiple(),
                                        required=True,
                                        error_messages={
                                            'required': _(
                                                "At least one criteria must"
                                                " be specified.")},
                                        help_text=_("Create repository"
                                                    " on instances from those groups"))

    def __init__(self, request, *args, **kwargs):

        super(SetScopeForNewRpmRepositoryDetailsAction, self).__init__(request, *args, **kwargs)

        groups_tuple = []

        for group in get_groups():

            groups_tuple.append((str(group.id),str(group.id)))

        if groups_tuple:

            self.fields['group_multiselect'].choices=groups_tuple
                    
                    


    class Meta(object):
        name = _("Scope")


class SetRepositoryChoice(workflows.Step):

    action_class = SetRpmRepositoryDetailsAction

    template_name = "patch_management/repositories/_details.html"

    def contribute(self, data, context):


        if (data.get("repository_type","") == "yum"):

            context['repo']=data.get("repo","")
            context['name']=data.get("name","")
            context['baseurl']=data.get("baseurl","")
            context['mirrorlist']=data.get("mirrorlist","")
            context['repository_type']=data.get("repository_type","")

            return context

        elif (data.get("repository_type","") == "zypper"):

            context['repo']=data.get("repo","")
            context['baseurl']=data.get("baseurl","")
            context['enabled']=data.get("enabled","")
            context['refresh']=data.get("refresh","")
            context['cache']=data.get("cache","")
            context['gpgcheck']=data.get("gpgcheck","")
            context['gpgautoimport']=data.get("gpgautoimport","")
            context['repository_type']=data.get("repository_type","")

            return context
        
        else:

            return context
    

class SetScopeForNewRpmRepositoryChoice(workflows.Step):

    action_class = SetScopeForNewRpmRepositoryDetailsAction

    contributes = ('grainpair',)

    template_name = "patch_management/repositories/_scope.html"

    def contribute(self, data, context):

        context['grainpairmultiselect']=data.get('grainpairmultiselect',"")
        context['group_multiselect']=data.get('group_multiselect',"")
 
        return context



class CreateRpmRepository(workflows.Workflow):

    slug = "create_repository"

    name = _("Create Repository")

    finalize_button_name = _("Create")

    success_message = _('Scheduled repository creating "%s".')

    failure_message = _('Unable to create repository "%s".')

    success_url = "horizon:patch_management:repositories:index"

    default_steps = (SetRepositoryChoice,SetScopeForNewRpmRepositoryChoice)

    @sensitive_variables('context')
    def handle(self, request, context):

        print '<: context :>'
        print context
        print '----------------'
        print dir(context)
        print '::::::::::::::::'

        if (context.get('repository_type','')=='zypper'):

            #get_group_members 
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

        elif (context.get('repository_type','')=='yum'):

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


        else: 

            pass
