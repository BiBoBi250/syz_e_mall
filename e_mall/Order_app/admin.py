from django.contrib import admin
from .models.order_models import Order
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import messages


# Register your models here.

# 自定义过滤器

class Generate_timeFilter(admin.SimpleListFilter):
    """根据订单产生时间查找"""
    # 用于查询的字段名
    parameter_name = 'generate_time'

    # 在查询选项上显示可读的文字
    title = _('搜索订单时间范围')

    def lookups(self, request, model_admin):
        """设置搜索项"""
        # 返回元祖列表，第一个元素用于搜索项，第二个元素用于将搜索项转换成可读的文字
        return [
            ('1_hour', _('一小时内')),
            ('1_day', _('一天内')),
            ('7_days', _('一周内')),
            ('1_month', _('一个月内')),
            ('3_month', _('三个月内')),
            ('6_month', _('半年内')),
            ('1_year', _('一年内'))
        ]

    def queryset(self, request, queryset):
        """针对不同搜索项，匹配不同数据"""
        # 通过self.value()取得匹配项
        if self.value() == '1_hour':
            return queryset.filter(generate_time__gte=(datetime.now() - timedelta(hours=1)),
                                   generate_time__lte=(datetime.now()))
        elif self.value() == '1_day':
            return queryset.filter(generate_time__gte=(datetime.now() - timedelta(days=1)),
                                   generate_time__lte=(datetime.now()))
        elif self.value() == '7_days':
            return queryset.filter(generate_time_gte=(datetime.now() - timedelta(days=7)),
                                   generate_time_lte=(datetime.now()))
        elif self.value() == '1_month':
            return queryset.filter(generate_time_gte=(datetime.now() - relativedelta(month=1)),
                                   generate_time_lte=(datetime.now()))
        elif self.value() == '3_month':
            return queryset.filter(generate_time_gte=(datetime.now() - relativedelta(month=3)),
                                   generate_time_lte=(datetime.now()))
        elif self.value() == '1_year':
            return queryset.filter(generate_time_gte=(datetime).now() - relativedelta(year=1),
                                   generate_time_lte=(datetime).now())
        else:
            return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ('commodity_name', 'commodity_category', 'quantity', 'generate_time', 'check_time', 'colored_status')
    # 字段超链接,连接到详情页面
    list_display_links = ('commodity_name', 'colored_status')
    # 搜寻字段
    search_fields = ('colored_status',)
    # 过滤字段
    list_filter = (Generate_timeFilter,)
    # 每页显示项数
    list_per_page = 20
    # 对一对N，一对一的model进行inner join的优化，也就是一次性搜索出来，然后再搜索外键的时候，不需要在查询数据库了
    # 默认该值为False，即参照list_display中的字段进行inner join。
    # list_select_related =('commodity')

    # ordering =(,),该字段应该与model的ordering一样
    ordering = ('-generate_time',)
    # 只读字段,必须在fileds中显示指定
    # readonly_fields = ('quantity', 'commodity', 'belong_shopper', 'shopping_trolley')

    actions = ['make_Checked', 'make_Unchecked']

    # 写在admin中，模型实例用obj代替
    def commodity_name(self, obj):
        '''返回商品的名称'''
        return obj.commodity.commodity_name

    def commodity_category(self, obj):
        '''返回商品的种类'''
        return obj.commodity.category

    def has_add_permission(self, request):
        '''取消所有商家增加订单的功能'''
        return False

    def make_Checked(self, request, querysets):
        """自定义审核完成动作"""
        result = querysets.update(check_status='Checked')
        if result == 1:
            message_shorthand = '1 order was checked'
        else:
            message_shorthand = '{} orders were checked'.format(result)
        # 左侧划出的提示框,level作为消息级别，引用django.contrib.message消息后端
        self.message_user(request, message_shorthand, level=messages.SUCCESS)

    def get_readonly_fields(self, request, obj=None):
        """根据是否审核，锁定审核订单"""
        if hasattr(obj, 'check_status') and \
                self.has_change_permission(request, obj) and self.has_view_permission(request, obj):
            if obj.check_status == 'Checked':
                self.readonly_fields = (
                    'belong_shopper', 'shopping_trolley', 'generate_time', 'check_time', 'status_choice',
                    'check_status', 'quantity', 'commodity')
            elif obj.check_status == 'Unchecked':
                self.readonly_fields =()


    make_Checked.short_description = '审核'
    make_Checked.type = 'success'
    make_Checked.confirm = '您确定要审核选中的项嘛？'

    def make_Unchecked(self, request, querysets):
        """自定义审核取消动作"""
        result = querysets.update(check_status='Unchecked')
        if result == 1:
            messages_shorthand = '1 order was unchecked'
        else:
            messages_shorthand = '{} orders were unchecked'.format(result)
        self.message_user(request, messages_shorthand, level=messages.SUCCESS)

    make_Unchecked.short_description = '取消审核'
    make_Unchecked.type = 'warning'
    # 确认按钮
    make_Unchecked.confirm = '您确定要取消审核选中的项嘛？'
