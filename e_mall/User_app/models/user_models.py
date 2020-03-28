from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Consumer(models.Model):
    """用户表"""
    # 用户名
    consumer = models.OneToOneField(User,
                                    verbose_name=_('消费者'),
                                    on_delete=models.CASCADE,
                                    related_name='consumer',
                                    )
    # 注册日期
    register_time = models.DateTimeField(auto_now_add=True, verbose_name=_('注册日期'))
    # 性别
    sex_choice = (
        ('f', '女'),
        ('m', '男'),
    )
    sex = models.CharField(verbose_name=_('性别'),
                           help_text=_('Please enter user'),
                           max_length=1,
                           choices=sex_choice,
                           )
    # 头像,会上传到media中的head目录下，不需要下划线，因为setting中的media已经有下划线了,
    head_image = models.ImageField(verbose_name=_('头像'),
                                   help_text=('Please upload your portrait'),
                                   upload_to='head',
                                   blank=True,
                                   )
    # 手机号，必须
    telephone = models.CharField(verbose_name=_('手机号'),
                                 help_text=_('Please write your cell-phone number'),
                                 unique=True,
                                 error_messages={
                                     'unique': _('A telephone number with this already exists.'),
                                 },
                                 max_length=11
                                 )
    consumer_ = Manager()

    class Meta:
        verbose_name = _('消费者')
        verbose_name_plural = _('消费者')

    def __str__(self):
        return self.username
