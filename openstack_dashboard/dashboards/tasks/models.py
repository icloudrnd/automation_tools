#
#
# db model for completed tasks
#
#
from django.db import models

class Jids(models.Model):
    jid = models.CharField(primary_key=True, max_length=20)
    load = models.TextField()

    class Meta:
        managed = False
        db_table = 'jids'
        app_label = 'fetch_data'


class SaltReturns(models.Model):
    added = models.DateTimeField(blank=True, null=True)
    fun = models.TextField()
    jid = models.CharField(max_length=20)
    return_field = models.TextField(db_column='return')  # Field renamed because it was a Python reserved word.
    id = models.TextField(primary_key=True)
    success = models.NullBooleanField()
    full_ret =  models.TextField()

    class Meta:
        managed = False
        db_table = 'salt_returns'
        app_label = 'fetch_data'
