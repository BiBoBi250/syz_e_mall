from django.contrib import admin, messages
# Register your models here.
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from Shopper_app.models.shopper_models import Store, Shoppers
from Shop_app.models.commodity_models import Commodity


class Putaway_status(admin.SimpleListFilter):
    """上架状态过滤器"""
    parameter_name = 'status'
    title = _('查询商品状态')

    def lookups(self, request, model_admin):
        return [
            ('Unshelve', _('下架状态')),
            ('Shelve', _('上架状态')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Unshelve':
            return queryset.filter(status='Unshelve')
        elif self.value() == 'Shelve':
            return queryset.filter(status='Shelve')


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    exclude = ('store', 'shopper')  # 不在form中显示
    list_display = ('commodity_name', 'price', 'intro', 'colored_status', 'store', 'shopper',)
    list_display_links = ('commodity_name',)
    list_per_page = 30
    # model中自定义的colored_status无法用于排序和修改
    # list_editable = ('colored_status',)
    list_filter = (Putaway_status,)
    # ordering = ('colored_status',)
    actions_on_top = True
    actions = ['make_shelve', 'make_unshelve']
    search_fields = ['category', ]

    '''
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """根据不同用户筛选其对应的数据，重新生成modelform"""
        # db_field.name 获取model的字段
        # 查找出店家的所有信息
        if db_field.name == 'store':
            # 店家
            user = User.objects.get(username=request.user.username)
            shopper = Shoppers.shoppers_.get(user=user)
            kwargs['queryset'] = Commodity.commodity_.filter(shopper=shopper)
        return super().formfield_for_dbfield(db_field,request,**kwargs)
    '''

    def save_model(self, request, obj, form, change):
        """保存对象后的自动添加商铺和用户"""
        # 使用多对一，1对1的select_related优化查询
        # Commodity.commodity_.select_related('shopper__user')
        # 使用多对多，1对多的prefetch_related优化查询
        # Shoppers.shoppers_.prefetch_related('commodity__store')
        # result = self.get_queryset(request).select_related('shopper__user').first()
        obj.store = Shoppers.shoppers_.get(user=request.user).store
        obj.shopper = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """每个用户只允许查看自己的上架的商品信息"""
        result = super().get_queryset(request).filter(shopper=request.user)
        return result

    def make_shelve(self, request, queryset):
        """更新下架动作"""
        try:
            result = queryset.update(status='Onshelve')
            if result == 1:
                message_shorthand = _('一个商品已经上架')
            else:
                message_shorthand = _('{} 个商品已经上架'.format(result))
                # 左侧划出的提示框,level作为消息级别，引用django.contrib.message消息后端
            self.message_user(request, message_shorthand, level=messages.SUCCESS)
        except:
            self.message_user(request, '上架商品操作失败，请联系管理员解决', level=messages.ERROR)

    def get_readonly_fields(self, request, obj=None):
        """根据商品的上架状态设定其是否可以修改"""
        # obj为注册的model
        if hasattr(obj, 'status') and self.has_view_or_change_permission(request, obj):
            if obj.status == 'Unshelve':
                self.readonly_fields = ()
            elif obj.status == 'Onshelve':
                self.readonly_fields = (
                'store', 'shopper', 'commodity_name', 'price', 'details', 'intro', 'category', 'status')

    make_shelve.short_description = '上架'
    # 自定义按钮图标
    make_shelve.icon = 'fas fa-audio-description'
    # 自定义按钮格式
    make_shelve.type = 'success'

    def make_unshelve(self, request, queryset):
        """更新上架动作"""
        try:
            result = queryset.update(status='Unshelve')
            if result == 1:
                message_shorthand = _('一个商品已经下架')
            else:
                message_shorthand = _('{} 个商品已经下架'.format(result))
                # 左侧划出的提示框,level作为消息级别，引用django.contrib.message消息后端
            self.message_user(request, message_shorthand, level=messages.SUCCESS)
        except:
            self.message_user(request, '下架商品操作失败，请联系管理员解决', level=messages.ERROR)

    make_unshelve.short_description = '下架'
    # 自定义按钮图标
    make_unshelve.icon = 'fas fa-audio-description'
    # 自定义按钮格式
    make_unshelve.type = 'warning'
