from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django import template

#
from django.core.urlresolvers import reverse

from horizon import tables,exceptions

#
# actions

#from openstack_dashboard.api.salt_api import delete_task,install_packages


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, post_id):
        pass

class CreateRepository(tables.LinkAction):

    name = "create"
    verbose_name = _("Create Repository")
    url = "horizon:patch_management:repositories:create"
    classes = ("ajax-modal", "btn-resize")


def get_Options_Yum(instance):

    template_name = 'patch_management/repositories/_options_yum.html'

    context = {'id' : instance.id, 
               'enabled' : instance.enabled,
               'failovermethod' : instance.failovermethod,
               'gpgcheck' : instance.gpgcheck,
               'metadata_expire' : instance.metadata_expire,
               'skip_if_unavailable' : instance.skip_if_unavailable }

    return template.loader.render_to_string(template_name, context)

def get_Options_Zypper(instance):

    template_name = 'patch_management/repositories/_options_zypper.html'

    context = {'id' : instance.id,
               'autorefresh' : instance.autorefresh,
               'cache' : instance.cache,
               'enabled' : instance.enabled,
               'gpgcheck' : instance.gpgcheck,
               'gpgautoimport' : instance.gpgautoimport,
               'keeppackages' : instance.keeppackages,
               'priority' : instance.priority,
               'refresh' : instance.refresh,
               'type' : instance.type }

    return template.loader.render_to_string(template_name, context)



class ModifyRepositoryMembersLink(tables.LinkAction):
    name = "modify_repository_members"
    verbose_name = _("Modify Repository Members")
    url = "horizon:groups:instances:modify_repository_members"
    #classes = ("ajax-modal",)
    icon = "plus"

    def get_link_url(self, datum=None):

        repository_id = getattr(datum,'id')

        url = "horizon:patch_management:repositories:modify_repository_members"

        return reverse(url, args=(repository_id,))



def get_Comments(instance):

    template_name = 'patch_management/repositories/_comments.html'

    context = {'id' : instance.id,
               'comments' : instance.comments }

    return template.loader.render_to_string(template_name, context)





class YumRepositoriesTable(tables.DataTable):

    id = tables.Column("id",  verbose_name = _("Repository Name"))
    name = tables.Column("name",  verbose_name = _("name"))
    options = tables.Column(get_Options_Yum,  verbose_name = _("Options"))
    comments = tables.Column(get_Comments,  verbose_name = _("Comments"))
    failovermethod = tables.Column("failovermethod",  verbose_name = _("Failovermethod"))
    file = tables.Column("file",  verbose_name = _("file"))
    gpgkey = tables.Column("gpgkey",  verbose_name = _("gpgkey"))
    metalink = tables.Column("metalink",  verbose_name = _("metalink"))


    class Meta:

        name = "yumrepositories"
        verbose_name = _("Yum Repositories")
        hidden_title = False
        #row_actions = (InstanceUpgradesLink,)
        row_actions = (ModifyRepositoryMembersLink,)
        table_actions = (CreateRepository,)
        package_manager_name = "yum"

class ZypperRepositoriesTable(tables.DataTable):

    id = tables.Column("id",  verbose_name = _("Repository Name"))
    name = tables.Column("name",  verbose_name = _("name"))
    options = tables.Column(get_Options_Zypper,  verbose_name = _("Options"))
    alias = tables.Column("alias",  verbose_name = _("alias"))
    baseurl = tables.Column("baseurl",  verbose_name = _("baseurl"))
    mirrorlist = tables.Column("mirrorlist",  verbose_name = _("mirrorlist")) 
    url = tables.Column("url",  verbose_name = _("url"))
    metadataPath = tables.Column("metadataPath",  verbose_name = _("metadataPath"))
    packages = tables.Column("packagesPath",  verbose_name = _("packagesPath"))


    class Meta:

        name = "zypperrepositories"
        verbose_name = _("Zypper Repositories")
        hidden_title = False
        #row_actions = (InstanceUpgradesLink,)
        row_actions = (ModifyRepositoryMembersLink,)
        table_actions = (CreateRepository,)
        package_manager_name = "zypper"

class DebRepositoriesTable(tables.DataTable):

    id = tables.Column("id",  verbose_name = _("Repository Name"))
    architectures = tables.Column("architectures",  verbose_name = _("Architectures"))
    comps = tables.Column("comps",  verbose_name = _("Comps"))
    disabled = tables.Column("disabled",  verbose_name = _("Disabled"))
    repo_file = tables.Column("repo_file",  verbose_name = _("File"))
    line = tables.Column("line",  verbose_name = _("Line"))
    repo_type = tables.Column("repo_type",  verbose_name = _("Type"))
    uri = tables.Column("uri",  verbose_name = _("Uri"))


    class Meta:

        name = "debrepositories"
        verbose_name = _("Deb Repositories")
        hidden_title = False
        #row_actions = (InstanceUpgradesLink,)




class RepositoryMembersTable(tables.DataTable):


    id = tables.Column("id",  verbose_name = _("Member"))

    class Meta:
        name = "repository_members"
        verbose_name = _("Repository Members")
        #table_actions = (AddMemberLink,DeleteMembersAction)
        #row_actions = (ModifyRepositoryMembersLink,)
        #row_class = UpdateMemberRow


