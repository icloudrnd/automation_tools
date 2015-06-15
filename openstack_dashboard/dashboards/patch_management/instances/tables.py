from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

#
from django.core.urlresolvers import reverse

from horizon import tables,exceptions

#
# actions

from openstack_dashboard.api.salt_api import delete_task,install_packages


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, post_id):
        pass

class InstallPackages(tables.BatchAction):
    name = "install_packages"

    verbose_name = _("Install packages")

    classes = ('btn-danger')

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Creating installation job",
            u"Creating installation jobs",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Installation job was created",
            u"Installation jobs were created",
            count
        )

    def multiple(self, data_table, request, object_ids):


        selected_packages = []

        for object_id in object_ids:

            package = data_table.get_object_by_id(object_id)

            selected_packages.append({package.id:package.version})

        full_url=request.get_full_path()

        instance_name=full_url.split('/')[-1:][0]

        install_packages(instance_name,selected_packages)



class InstanceUpgradesLink(tables.LinkAction):
    name = "upgrade"
    verbose_name = _("Upgrade")
    url = "horizon:patch_management:instances:upgrade"
    classes = ("btn-sm","btn-danger")
    icon = "pencil"

    def get_link_url(self, instance):

        return "/patch_management/upgrade_packages/"+instance.id




class InstanceTable(tables.DataTable):

    id = tables.Column("id",  verbose_name = _("Instance Name"))

    os = tables.Column("os",  verbose_name = _("OS"))

    class Meta:

        name = "instance"
        verbose_name = _("Instances")
        row_actions = (InstanceUpgradesLink,)


class PackagesForUpgradeTable(tables.DataTable):

    id = tables.Column("id",  verbose_name = _("Name"))

    version = tables.Column("version", verbose_name = _("Version"))

    class Meta:
        name = "package_for_upgrade"
        verbose_name = _("Packages for Upgrade")
        table_actions = (InstallPackages,)
