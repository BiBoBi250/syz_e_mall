from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager
# Create your models here.
from django.utils.html import format_html

from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField
from Shopper_app.models.shopper_models import Store, Shoppers
from User_app.models.user_models import Consumer


class Shopping_trolley(models.Model):
    """购物车表"""
    # 商品数量
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'),
                                           help_text=_('The quantity of this goods'),
                                           default=0,
                                           )
    # 用户
    user = models.OneToOneField(Consumer,
                                verbose_name='用户',
                                help_text=('购物车归属的用户'),
                                on_delete=models.CASCADE,
                                related_name='shopping_trolley'
                                )

    # 商品简单描述
    intro = models.TextField(verbose_name=_('content'),
                             help_text=_('A briefly describe'))

    # 商品价格,正整数
    price = models.PositiveIntegerField(verbose_name=_('商品价格'),
                                        help_text=_('Please enter the price of the goods'),
                                        )
    # 商品名称
    commodity_name = models.CharField(verbose_name=_('商品名'),
                                      help_text=_('Please enter the name of the product'),
                                      max_length=100,
                                      )

    # 店铺名
    store_name = models.CharField(verbose_name=_('店铺名'),
                                  help_text=_('the definition name of store'),
                                  max_length=30,
                                  unique=True,
                                  )
    # 商品过期状态
    store = models.BooleanField(verbose_name=_('商品上架状态'),
                                help_text=_('商品上架还是下架，店铺存在还是不存在'),
                                default=True)


    class Meta:
        verbose_name = _('购物车')
        verbose_name_plural = _('购物车')

    def __str__(self):
        return '{}用户的购物车'.format(self.user)


class Commodity(models.Model):
    """商品表"""
    # 店铺
    store = models.ForeignKey(Store,
                              verbose_name=_('商铺'),
                              help_text='商品所在的店铺',
                              on_delete=models.CASCADE,
                              related_name='commodity',
                              )
    # 店家
    shopper = models.ForeignKey(User,
                                verbose_name=_('商家'),
                                help_text='商品所属的商家',
                                on_delete=models.CASCADE,
                                related_name='commodity',
                                )

    # 商品名称
    commodity_name = models.CharField(verbose_name=_('商品名称'),
                                      help_text=_('Please enter the name of the product'),
                                      max_length=100,
                                      )
    # 商品价格,正整数
    price = models.PositiveIntegerField(verbose_name=_('价格'),
                                        help_text=_('Please enter the price of the goods'),
                                        )
    # 商品详细描述
    details = MDTextField(verbose_name=_('商品的详细描述'),
                          help_text=_('Please describe your product in detail'))

    # 商品简单描述
    intro = models.TextField(verbose_name=_('商品的简要描述'),
                             help_text=_('A briefly describe'))

    # 商品种类
    commodity_choice = (
        ('衣服', '衣服'),
        ('裤子', '裤子'),
        ('鞋子', '鞋子'),
        ('电子设备', '电子设备'),
        ('化妆品', '化妆品'),
        ('食品', '食品')
    )
    category = models.CharField(verbose_name=_('商品类别'),
                                help_text=_('Please select the type of goods'),
                                max_length=10,
                                choices=commodity_choice,
                                )
    # 上架状态
    shelve_state = (
        ('Unshelve', '下架'),
        ('Onshelve', '上架'),
    )
    status = models.CharField(verbose_name='上架状态',
                              help_text=_('Please select the sale status'),
                              max_length=10,
                              choices=shelve_state,
                              )
    commodity_ = Manager()

    class Meta:
        verbose_name = _('商品表')
        verbose_name_plural = _('商品表')

    def __str__(self):
        return '商品：{}'.format(self.commodity_name)

    def colored_status(self):
        """替换状态颜色"""
        global color_code
        if self.status == 'Unshelve':
            color_code = '#E92B34'
        elif self.status == 'Onshelve':
            color_code = '#5DECA5'
        # display_name = self.get_status_display()
        return format_html(
            '<span style="color:{};font-size:16px;font-weight:bolder;">{}</span>',
            color_code,
            self.status,
        )


class Inventory(models.Model):
    """库存表"""
    # 商家
    user = models.OneToOneField(User, verbose_name=_('商家'),
                                help_text=_('您'),
                                on_delete=models.CASCADE,
                                related_name='user',
                                )
    # 库存
    commodity = models.ForeignKey(Commodity,
                                  verbose_name=_('商品'),
                                  help_text='库存中的商品',
                                  on_delete=models.CASCADE,
                                  related_name='inventory',
                                  )
    # 商品库存，正整数
    repository = models.PositiveIntegerField(verbose_name=_('库存量'),
                                             help_text=_('Please enter the inventory of the goods'),
                                             )
    # 进货量
    purchase_number = models.PositiveIntegerField(verbose_name=_('进货数量'),
                                                  help_text=_('Please fill in the quantity of purchase'),
                                                  )
    # 进货时间
    purchase_time = models.DateTimeField(auto_now=True, verbose_name=_('进货时间'))

    class Meta:
        verbose_name = _('库存表')
        verbose_name_plural = _('库存表')

    def __str__(self):
        return '您的库存'
