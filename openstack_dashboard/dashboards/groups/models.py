#
#
# db model for completed tasks
#
#
from django.db import models

class GroupMember(models.Model):

    member_name = models.CharField(max_length=100)

    member_type = models.CharField(max_length=100)

    member_group_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'group_members'
        app_label = 'fetch_data'

