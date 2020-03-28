from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Manager
# Create your models here.
from django.utils.translation import gettext_lazy as _


class Shoppers(models.Model):
    """店家表"""
    # shopper_name_validator = UnicodeUsernameValidator()
    # 与User1对1
    shopper = models.OneToOneField(User,verbose_name=_('商铺管理员'),
                                on_delete=models.CASCADE,
                                related_name='shopper')
    # 电话
    telephone = models.CharField(verbose_name=_('电话号码'), help_text=_('Please write your telephone'), blank=True,
                                 max_length=15)
    # 信誉
    # 通过get_字段_display()显示choice中的后半部分
    shop_credit_choice = (
        ('1星', '1星'),
        ('2星', '2星'),
        ('3星', '3星'),
        ('4星', '4星'),
        ('5星', '5星'),
        ('2钻', '2钻'),
        ('3钻', '3钻'),
        ('4钻', '4钻'),
        ('5钻', '5钻'),
    )
    shop_credit = models.CharField(verbose_name=_('信誉'),
                                   help_text=_('this display the rank of your credit on your shop'),
                                   choices=shop_credit_choice,
                                   default='1星',
                                   max_length=4
                                   )

    # 性别
    sex_choice = (
        ('m', '男'),
        ('f', '女'),
    )
    sex = models.CharField(verbose_name=_('性别'),
                           help_text=_('性别'),
                           blank=True,
                           choices=sex_choice,
                           max_length=1,
                           )
    # 头像
    head_image = models.ImageField(verbose_name=_('头像'),
                                   help_text=('Please upload your portrait'),
                                   upload_to='head',
                                   blank=True,
                                   )

    shoppers_ = Manager()

    class Meta:
        verbose_name = _('商家表')
        verbose_name_plural = _('商家表')

    def __str__(self):
        return self.shopper


class Store(models.Model):
    """店铺表"""
    # 店铺名称
    store_name = models.CharField(verbose_name=_('店铺'),
                                  help_text=_('Please personalize the definition name '),
                                  max_length=30,
                                  unique=True,
                                  error_messages={
                                      'unique': _("A Store with that store_name already exists."),
                                  },
                                  blank=True
                                  )
    # 商家表
    shopper = models.OneToOneField(User,
                                   verbose_name=_('商家'),
                                   help_text=_('Please write your name'),
                                   on_delete=models.CASCADE,
                                   related_name='store',
                                   )
    # 注册时间
    start_time = models.DateTimeField(verbose_name=_('注册时间'), auto_now_add=True)
    # 省份
    # 通过get_字段_display()显示choice中的后半部分
    province_choice = (

    )
    province = models.CharField(verbose_name=_('省份'),
                                help_text=_('Please select province'),
                                max_length=10,
                                choices=province_choice,
                                blank=True
                                )
    # 市
    city_choice = (

    )
    city_choice = models.CharField(verbose_name=_('城市'),
                                   help_text=_('Please select city'),
                                   max_length=20,
                                   choices=city_choice,
                                   blank=True
                                   )

    # 被关注量
    attention = models.PositiveIntegerField(verbose_name=_('关注量'),
                                            help_text=_('Store attention'),
                                            default=0,
                                            )

    # 店铺评分,max_digits表示最大位数，decimal_places=1表示精度（小数)位数
    shop_grade = models.DecimalField(verbose_name=_('shop grade'),
                                     help_text=_('Please write shop grade about this shop'),
                                     max_digits=2,
                                     decimal_places=1,
                                     default=0.0,
                                     )

    store_ = Manager()

    class Meta:
        verbose_name = _('店铺')
        verbose_name_plural = _('店铺')

    def __str__(self):
        return self.store_name

class Ip(models.Model):
    """Ip表"""
    # 登录总次数
    ips = models.CharField(verbose_name=_('ip地址'),
                           help_text=_('ip地址'),
                           max_length=12,
                           )
    # 当前日期
    login_time  = models.DateTimeField(verbose_name=_('上线时间'),
                                help_text=_('登录的时间'),
                                auto_now_add=True,
                                )
    # 商家
    shopper = models.ForeignKey(User,verbose_name=_('商家'),
                                help_text=_('商家'),
                                on_delete=models.CASCADE,
                                related_name='ip')
    # 下线时间
    exit_time = models.DateTimeField(verbose_name=_('下线时间'),
                                     help_text=_('退出网站的时间'),
                                     blank=True,
                                     )

    ip_ = Manager()

    class meta:
        ordering = ('-date')
        verbose_name = _('记录表')
        verbose_name_plural = _('记录表')


    def __str__(self):
        return self.shopper.username

