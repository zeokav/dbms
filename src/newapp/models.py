# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=160, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=510, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=256, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=60, blank=True, null=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.CharField(max_length=508, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BookingHistory(models.Model):
    person = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    pnr = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'booking_history'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=400, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=510, blank=True, null=True)
    name = models.CharField(max_length=510, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=80)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    mob_no = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Platform(models.Model):
    platform_id = models.IntegerField(primary_key=True)
    platform_name = models.CharField(max_length=50)
    xcoord = models.IntegerField()
    ycoord = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'platform'


class Pricing(models.Model):
    base_fare = models.FloatField(blank=True, null=True)
    cost_per_km = models.FloatField(blank=True, null=True)
    train = models.ForeignKey('Train', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pricing'


class Tickets(models.Model):
    pnr = models.IntegerField(primary_key=True)
    train = models.ForeignKey('Train', models.DO_NOTHING, blank=True, null=True)
    no_of_platforms = models.IntegerField(blank=True, null=True)
    journey_distance = models.FloatField(blank=True, null=True)
    date_of_journey = models.DateField(blank=True, null=True)
    startplatform_id = models.IntegerField(blank=True, null=True)
    endplatform_id = models.IntegerField(blank=True, null=True)
    person = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class Train(models.Model):
    train_name = models.CharField(max_length=30)
    train_id = models.IntegerField(primary_key=True)
    capacity = models.IntegerField(blank=True, null=True)
    startp_id = models.IntegerField(blank=True, null=True)
    endp_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'train'


class Visits(models.Model):
    train = models.ForeignKey(Train, models.DO_NOTHING, blank=True, null=True)
    platform = models.ForeignKey(Platform, models.DO_NOTHING, blank=True, null=True)
    departure_time = models.CharField(max_length=8)
    arrival_time = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'visits'
