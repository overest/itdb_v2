from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
# Create your models here.

class UserProfileManager(BaseUserManager):
    def create_user(self, username, email,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('用户名是必须的！')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(
        verbose_name='用户名',
        max_length=32,
        unique=True,
    )
    email = models.EmailField()
    office_place = models.ForeignKey('OfficePlace',related_name='office_place_user',verbose_name="办公地点",default='1')
    store_place = models.ManyToManyField('StorePlace', related_name='store_place_user', verbose_name="管理库存地点", default='1')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        verbose_name_plural = "用户信息"


class Level(models.Model):
    '''分类级别'''
    level_name = models.CharField(max_length=32,verbose_name="分类级别")

    def __str__(self):
        return self.level_name
    class Meta():
        verbose_name_plural = "分类级别"

class AssetAttr(models.Model):
    ''' 资产属性，如：固定资产、IP电话...'''
    asset_attr = models.CharField(max_length=64,verbose_name="资产分类")
    level = models.ForeignKey(Level,related_name='level_assettype',verbose_name='分类级别')
    def __str__(self):
        return self.asset_attr
    class Meta():
        verbose_name_plural = "资产属性"

class AssetModel(models.Model):
    '''资产类别，如：台式机、笔记本、显示器、IP电话、键盘、鼠标...'''
    asset_model = models.CharField(max_length=64,verbose_name="资产类别")
    asset_type = models.ForeignKey(AssetAttr,verbose_name='资产属性')
    level = models.ForeignKey(Level,verbose_name='分类级别')
    def __str__(self):
        return self.asset_model
    class Meta():
        verbose_name_plural = "资产类别"

class AssetProvider(models.Model):
    '''资产品牌，如：dell 、hp...'''
    provider = models.CharField(max_length=64,verbose_name="资产品牌")
    asset_model = models.ManyToManyField(AssetModel,verbose_name='资产类别')
    level = models.ForeignKey(Level,verbose_name='分类级别')
    def __str__(self):
        return self.provider
    class Meta():
        verbose_name_plural = "资产品牌"

class DeviceModel(models.Model):
    '''设备型号'''
    model_name = models.CharField(max_length=64,verbose_name="设备型号")
    provider = models.ForeignKey(AssetProvider,verbose_name='资产品牌')
    product_conf = models.ForeignKey('ProductConf',verbose_name="配置信息")

    def __str__(self):
        return self.model_name
    class Meta():
        verbose_name_plural = "设备型号"

class ProductConf(models.Model):
    product_conf = models.CharField(max_length=64,verbose_name="配置信息",default=' N/A ')
    # model_name = models.ForeignKey(DeviceModel,verbose_name='设备型号')
    def __str__(self):
        return self.product_conf
    class Meta():
        verbose_name_plural = "配置信息"

class AssetName(models.Model):
    '''资产名称'''
    asset_name = models.CharField(max_length=32,verbose_name="资产名称")
    model_name = models.ManyToManyField(DeviceModel,verbose_name='设备型号')

    def __str__(self):
        return self.asset_name
    class Meta():
        verbose_name_plural = "资产名称"

class OfficePlace(models.Model):
    '''办公地点'''

    office_place = models.CharField(max_length=32,verbose_name="办公地点",unique=True)

    def __str__(self):
        return self.office_place

    class Meta():
        verbose_name_plural = "办公地点"

class StorePlace(models.Model):
    '''库存地点'''
    store_place = models.CharField(max_length=32,verbose_name="库存地点")
    office_place = models.ForeignKey(OfficePlace,verbose_name='办公地点')
    def __str__(self):
        return self.store_place
    class Meta():
        verbose_name_plural = "库存地点"

class UseType(models.Model):
    '''使用类型'''
    use_type = models.CharField(max_length=32,verbose_name="使用类型")

    def __str__(self):
        return self.use_type

    class Meta():
        verbose_name_plural = "使用类型"

class AssetStatus(models.Model):
    '''资产状态'''
    asset_status = models.CharField(max_length=32,verbose_name="资产状态")
    def __str__(self):
        return self.asset_status

    class Meta():
        verbose_name_plural = "资产状态"

class InStock(models.Model):
    '''库存状态'''
    in_stock = models.ManyToManyField(AssetStatus,verbose_name='库存状态')

    class Meta():
        verbose_name_plural = "库存状态"

class NonStock(models.Model):
    '''非库存状态'''
    non_stock = models.ManyToManyField(AssetStatus,verbose_name="非库存状态")

    class Meta():
        verbose_name_plural = "非库存状态"

class InOutReasons(models.Model):
    '''出入库原因'''
    in_out_reasons = models.CharField(max_length=32,verbose_name="出入库原因")
    def __str__(self):
        return self.in_out_reasons

    class Meta():
        verbose_name_plural = "出入库原因"

class InReasons(models.Model):
    '''入库原因'''
    in_reasons =  models.ManyToManyField(InOutReasons,verbose_name="入库原因")
    class Meta():
        verbose_name_plural = "入库原因"

class OutReasons(models.Model):
    '''出库原因'''
    out_reasons = models.ManyToManyField(InOutReasons, verbose_name="出库原因")


    class Meta():
        verbose_name_plural = "出库原因"

class Supplier(models.Model):
    '''供应商'''
    supplier = models.CharField(max_length=64,verbose_name="供应商")

    def __str__(self):
        return self.supplier
    class Meta():
        verbose_name_plural = "供应商"

class CheckInfo(models.Model):
    '''盘点信息'''
    title = models.CharField(max_length=32,verbose_name="Title",default="N/A")
    check = models.NullBooleanField("是否盘点")
    check_time = models.DateTimeField(editable=True,verbose_name="盘点时间",null=True,blank=True)
    check_remark  = models.CharField(max_length=256,verbose_name="盘点异常备注",null=True,blank=True)
    class Meta():
        verbose_name_plural = '盘点信息'
    def __str__(self):
        return self.title

class AssetInfo(models.Model):
    asset_id = models.CharField(max_length=164, verbose_name="资产编号",primary_key=True)
    sn = models.CharField(max_length=128, verbose_name="资产序列号（S/N）")
    mac_addr = models.CharField(max_length=32, verbose_name='MAC地址', null=True, blank=True)
    level = models.ForeignKey(Level, verbose_name='分类级别')
    asset_attr = models.ForeignKey(AssetAttr, verbose_name='资产属性')
    asset_model = models.ForeignKey(AssetModel, verbose_name="资产类别")
    asset_provider = models.ForeignKey(AssetProvider, verbose_name="品牌")
    device_model = models.ForeignKey(DeviceModel, verbose_name="设备型号")
    product_conf = models.ForeignKey(ProductConf, verbose_name='配置信息')
    asset_name = models.ForeignKey(AssetName, verbose_name='资产名称')
    office_place = models.ForeignKey(OfficePlace,verbose_name='办公地点')
    store_place = models.ForeignKey(StorePlace, verbose_name='库存地点')
    use_type = models.ForeignKey(UseType, verbose_name="使用类型")
    asset_status = models.ForeignKey(AssetStatus, verbose_name='资产状态')
    in_out_reason = models.ForeignKey(InOutReasons, verbose_name='出入库原因')
    supplier = models.ForeignKey(Supplier, verbose_name='供应商')
    last_check_time = models.ForeignKey(CheckInfo,verbose_name="上一次盘点时间",default='3')
    user_name = models.ForeignKey(UserProfile, related_name='user_name_appleset', verbose_name='使用人')
    owner = models.ForeignKey(UserProfile, related_name='owner_appleset', verbose_name='责任人')
    operator = models.ForeignKey(UserProfile, related_name='operator_appleset', verbose_name='最近操作人')
    company_info = models.CharField(max_length=128, verbose_name="公司信息")
    buy_time = models.DateTimeField(default=timezone.now,editable=True,verbose_name='购买时间')
    create_time = models.DateTimeField(default=timezone.now,editable=True,verbose_name='创建时间')
    # update_time = models.DateTimeField(editable=True,default=timezone.now,verbose_name='更新时间')
    update_time = models.DateTimeField(auto_now=True ,verbose_name='更新时间')
    up_time = models.DateTimeField(default=timezone.now,editable=True,verbose_name='启用时间')
    remark = models.CharField(max_length=256,verbose_name="备注",null=True,blank=True)

    def __str__(self):
        return self.asset_id

    class Meta():
        verbose_name_plural = "资产详情"

class OperationLogs(models.Model):
    """操作日志"""
    type_choices = (
        (0, "新增入库"),
        (1, "新增出库")
    )
    asset_id = models.CharField(max_length=64, verbose_name="资产编号")
    type = models.IntegerField(choices=type_choices)
    before_field = models.TextField(verbose_name="修改前字段信息",null=True)
    operator = models.ForeignKey(UserProfile, verbose_name='最近操作人')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
    after_field = models.TextField(verbose_name="修改后字段信息", null=True)


    class Meta():
        verbose_name_plural = "操作日志"
        ordering = ['update_time']