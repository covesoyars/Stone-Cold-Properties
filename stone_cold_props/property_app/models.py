# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Address(models.Model):
    building = models.ForeignKey('Building', models.DO_NOTHING, db_column='Building_ID', primary_key=True)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=30, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=20, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zip = models.DecimalField(db_column='Zip', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Address'


class AppartmentBuilding(models.Model):
    building = models.ForeignKey('Building', models.DO_NOTHING, db_column='Building_ID', primary_key=True)  # Field name made lowercase.
    number_units = models.DecimalField(db_column='Number_Units', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    available_units = models.DecimalField(db_column='Available_Units', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Appartment_Building'


class Building(models.Model):
    building_id = models.DecimalField(db_column='Building_Id', primary_key=True, max_digits=4, decimal_places=0)  # Field name made lowercase.
    floors = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Building'


class Client(models.Model):
    ssn = models.CharField(db_column='SSN', primary_key=True, max_length=11)  # Field name made lowercase.
    first_name = models.CharField(db_column='First_Name', max_length=15, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Client'


class Contract(models.Model):
    ssn = models.ForeignKey(Client, models.DO_NOTHING, db_column='SSN', primary_key=True)  # Field name made lowercase.
    building = models.ForeignKey(Building, models.DO_NOTHING, db_column='Building_ID')  # Field name made lowercase.
    payment = models.DecimalField(db_column='Payment', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)  # Field name made lowercase.
    end_date = models.DateField(db_column='End_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Contract'
        unique_together = (('ssn', 'building'),)


class Lease(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    unit = models.DecimalField(max_digits=4, decimal_places=0)
    building = models.ForeignKey(Building, models.DO_NOTHING, db_column='building')
    tenant = models.CharField(primary_key=True, max_length=11)
    prop_man = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'Lease'
        unique_together = (('tenant', 'prop_man', 'building', 'unit'),)


class Level(models.Model):
    level = models.DecimalField(primary_key=True, max_digits=1, decimal_places=0)
    salary = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    commission = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Level'


class Manages(models.Model):
    ssn = models.CharField(primary_key=True, max_length=11)
    building = models.ForeignKey(Building, models.DO_NOTHING, db_column='building', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Manages'


class PropertyManager(models.Model):
    first_name = models.CharField(db_column='First_Name', max_length=15, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ssn = models.CharField(db_column='SSN', primary_key=True, max_length=11)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_Date', blank=True, null=True)  # Field name made lowercase.
    level = models.ForeignKey(Level, models.DO_NOTHING, db_column='Level', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Property_Manager'


class Tenant(models.Model):
    first_name = models.CharField(db_column='First_Name', max_length=15, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    income = models.DecimalField(db_column='Income', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ssn = models.CharField(db_column='SSN', primary_key=True, max_length=11)  # Field name made lowercase.
    account_balance = models.DecimalField(db_column='Account_balance', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    building_id = models.DecimalField(db_column='Building_ID', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tenant'


class Unit(models.Model):
    building = models.ForeignKey(Building, models.DO_NOTHING, db_column='Building_ID', primary_key=True)  # Field name made lowercase.
    sqft = models.DecimalField(db_column='SqFt', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    bedrooms = models.DecimalField(db_column='Bedrooms', max_digits=1, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    bathrooms = models.DecimalField(db_column='Bathrooms', max_digits=1, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rent = models.DecimalField(db_column='Rent', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    available = models.IntegerField(db_column='Available', blank=True, null=True)  # Field name made lowercase.
    unit_number = models.DecimalField(db_column='Unit_Number', max_digits=4, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Unit'
        unique_together = (('building', 'unit_number'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
