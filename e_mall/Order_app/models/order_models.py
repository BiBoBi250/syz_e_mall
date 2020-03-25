from django.db import models
from django.db.models import Manager
from Shopper_app.models.shopper_models import Shoppers
from Shop_app.models.commodity_models import Commodity, Shopping_trolley
# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

class Order(models.Model):
    """商品订单表"""
    # 对应的店家
    belong_shopper = models.ForeignKey(Shoppers,
                                       verbose_name='商家',
                                       help_text='该商品所对应的商家',
                                       on_delete=models.CASCADE,
                                       related_name='order',
                                       )
    # 购物车
    shopping_trolley = models.ForeignKey(Shopping_trolley,
                                         verbose_name=_('购物车'),
                                         help_text=_('Shopping trolley'),
                                         on_delete=models.CASCADE,
                                         related_name='order',
                                         )
    # 产生订单日期
    generate_time = models.DateTimeField(verbose_name=_('生成订单时间'), auto_now_add=True)
    # 审核订单完毕日期
    check_time = models.DateTimeField(verbose_name=_('审核完毕订单时间'), auto_now=True)
    # 审核状态
    # 通过get_字段_display()显示choice中的后半部分
    status_choice = (
        ('Unchecked', 'Unchecked'),
        ('Checked', 'Checked'),
    )
    check_status = models.CharField(verbose_name=_('审核状态'),
                                    help_text=_('Please check the order of customers'),
                                    choices=status_choice,
                                    default='Unchecked',
                                    max_length=20,
                                    )
    # 订单内商品数量
    quantity = models.PositiveIntegerField(verbose_name=_('商品数量'),
                                           help_text=_('Please check the quantity of the goods'),
                                           blank=True,
                                           )
    commodity = models.OneToOneField(Commodity,
                                     verbose_name=_('商品'),
                                     help_text=_('The goods corresponding to this order'),
                                     on_delete=models.CASCADE,
                                     related_name='order'
                                     )
    order_ = Manager()

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('order')
        ordering = ('-generate_time',)

    def colored_status(self):
        """替换订单状态字段颜色"""
        global  color_code
        if self.check_status == 'Unchecked':
            color_code = '#5DECA5',
        elif self.check_status == 'Checked':
            color_code = '#E92B34'
        # display_name = self.get_check_status_display()
        # self.shopping_trolley.intro
        return format_html(
            '<span style="color:{}";>{}</span>',
            color_code,
            self.check_status,
        )
    # 告诉admin按照 generate_time来排序
    colored_status.admin_order_field = '-generate_time'
    # 给字段添加可读的名字
    colored_status.short_description = "审核状态ss"




