from django.db import models
from Soft_Site.settings import BASE_DIR, STATIC_URL
from Soft_Loading.apps import SoftLoadingConfig


class MainCategory(models.Model):
    name = models.CharField(db_column='Name', unique=True, max_length=40)
    main_cat_id = models.AutoField(db_column='MainCatID', primary_key=True)

    class Meta:
        managed = False
        db_table = 'MainCategories'
        verbose_name_plural = 'Maincategories'


class SubCategory(models.Model):
    name = models.CharField(db_column='Name', max_length=40)
    sub_cat_id = models.AutoField(db_column='SubCatID', primary_key=True)
    main_cat_id = models.ForeignKey(MainCategory, models.DO_NOTHING, related_name='sub_categories',
                                    db_column='MainCatID', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'SubCategories'
        verbose_name_plural = 'Subcategories'


class Platform(models.Model):
    name = models.CharField(db_column='Name', unique=True, max_length=40)
    platform_id = models.AutoField(db_column='PlatformID', primary_key=True)
    # icon = models.FileField(db_column='Path',
    #                         upload_to=BASE_DIR/SoftLoadingConfig.name/STATIC_URL/SoftLoadingConfig.name,
    #                         blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Platforms'


class Soft(models.Model):
    name = models.CharField(db_column='Name', max_length=70)
    description = models.TextField(db_column='Description', blank=True, null=True)
    image = models.TextField(db_column='Image', blank=True, null=True)
    is_primary = models.BooleanField(db_column='IsPrimary')  # Field name made lowercase.

    soft_id = models.AutoField(db_column='SoftID', primary_key=True)
    main_cat_id = models.ForeignKey(MainCategory, models.DO_NOTHING, db_column='MainCatID')
    sub_cat_id = models.ForeignKey(SubCategory, models.DO_NOTHING, db_column='SubCatID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Soft'
        verbose_name_plural = 'Soft'


class File(models.Model):
    size = models.CharField(db_column='Size',max_length=40)
    architecture = models.CharField(db_column='Architecture', max_length=10)
    version = models.CharField(db_column='Version', max_length=40, blank=True, null=True)
    compatibility = models.TextField(db_column='Compatibility')
    languages = models.TextField(db_column='Languages', blank=True, null=True)
    creator = models.CharField(db_column='Creator', max_length=40, blank=True, null=True)
    path = models.FileField(db_column='Path', upload_to='soft_versions/',
                            blank=True, null=True)

    file_id = models.AutoField(db_column='FileID', primary_key=True)
    soft_id = models.ForeignKey(Soft, models.DO_NOTHING,  db_column='SoftID', related_name='files')
    platform_id = models.ForeignKey(Platform, models.DO_NOTHING, db_column='PlatformID',
                                    related_name='files', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Files'


class History(models.Model):
    class Meta:
        managed = False
        db_table = 'History'
        verbose_name_plural = 'History'


class Subscription(models.Model):
    is_active = models.BooleanField(db_column='IsActive')
    is_paid = models.BooleanField(db_column='IsPaid')
    start_date = models.DateTimeField(db_column='StartDate')
    end_date = models.DateTimeField(db_column='EndDate')
    pay_date = models.DateTimeField(db_column='PayDate', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)

    subscr_id = models.AutoField(db_column='SubscrID', primary_key=True)
    user_uid = models.IntegerField(db_column='UserUID')
    manager_uid = models.IntegerField(db_column='ManagerUID')

    class Meta:
        managed = False
        db_table = 'Subscriptions'


class User(models.Model):
    mail = models.CharField(db_column='Mail', unique=True, max_length=40)
    login = models.CharField(db_column='Login', unique=True, max_length=40)
    password = models.CharField(db_column='Password', max_length=40)
    is_admin = models.BooleanField(db_column='IsAdmin')
    uuid = models.IntegerField(db_column='UUID', primary_key=True)

    is_active = models.BooleanField(db_column='IsActive', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=40, blank=True, null=True)
    surname = models.CharField(db_column='Sername', max_length=40, blank=True, null=True)
    telephone = models.CharField(db_column='Telephone', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'

