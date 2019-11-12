from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order

# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Tenant(models.Model):
    first_name = models.CharField(db_column='First_Name', max_length=15, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    income = models.DecimalField(db_column='Income', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ssn = models.CharField(db_column='SSN', primary_key=True, max_length=11)  # Field name made lowercase.
    account_balance = models.DecimalField(db_column='Account_balance', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    building_id = models.DecimalField(db_column='Building_ID', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=12, blank=True, null=True)  # Field name made lowercase.
    on_delete = models.CASCADE
    class Meta:
        managed = False       
        db_table = 'Tenant'

