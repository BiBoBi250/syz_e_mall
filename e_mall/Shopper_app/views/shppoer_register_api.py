from django.contrib.auth import login
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Shopper_app.models.shopper_models import Shoppers, Store, Ip
from django.http import Http404, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from ..views import tasks
from e_mall.authentication_rewrite import Email_or_Username
from e_mall.response_code import *
import logging

logger = logging.getLogger('shopper_app')  # 设置日志名
# 商家用户日志记录
logging.basicConfig(filename='Shopper_app/error.log',
                    level=logging.ERROR,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                    )  # 日志文件

# 响应状态实例
response_code = Response_code()

# 认证实例
email_or_username = Email_or_Username()

class Shopper_user_prem:
    """设置权限"""
    permissions_pub = [
        '',
    ]

    def set_shopper_perm(self, user):
        permissions = Permission.objects.filter(codename__in=self.permissions_pub)
        for permission in permissions:
            # 增加商家基本权限
            user.user_permissions.add(permission)


class Login(APIView):
    def post(self, request):
        """登录"""
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        login_id = request.data.get('login_id')
        password = request.data.get('password')
        # 认证用户
        try:
            shopper_auth = email_or_username.authenticate(request,login_id, password)
            user_status = True if shopper_auth else False
            if user_status:
                # 登录，传输session_id
                login(request, shopper_auth)
                Ip.ip_.create(ips=ip, shopper=shopper_auth)
                return JsonResponse(response_code.login_success)
            else:
                # 登录失败
                return JsonResponse(response_code.login_error)
        except Exception as e:
            # 将错误写进日志
            logger.error('login_error:{}'.format(str(e)))
            return JsonResponse(response_code.server_error)


class Register(APIView):
    def post(self, request):
        """注册"""
        ip = request.META.get('REMOTE_ADDR', 'unknown')  # 获取ip地址
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        telephone = request.data.get('phone')
        sex = request.data.get('sex')
        verification_code = request.data.get('verification_code')# 验证码
        # 商家基本权限
        shopper_user_prem = Shopper_user_prem()
        try:
            User.objects.get(username=username)
            # 存在用户
            # 返回Json格式字符串
            return JsonResponse(response_code.user_existed)
        except User.DoesNotExist:
            # 可以注册
            exists = False
            code_status = True if verification_code == request.session['verification_code'] else False
            if not code_status:
                return JsonResponse(response_code.verification_code_error)
        except Exception as e:
            # 服务器错误
            logger.error('Login_error:{}'.format(str(e)))
            return JsonResponse(response_code.register_error)
        if not exists:
            try:
                # 额外参数
                extra_fields = {
                    'is_staff': True,
                    'is_superuser': False,
                    'is_active': True
                }
                # 创建商家
                shopper = User.objects.create_user(username=username, email=email, password=password,
                                                   **extra_fields)
                # 创建商家其他信息
                Shoppers.shoppers_.create(shopper=shopper, telephone=telephone, sex=sex)
                # 为每一个商家创建一个店铺
                Store.store_.create(shopper=shopper)
                # 认证用户
                shopper_auth = email_or_username.authenticate(request, username, password)
                # 设置权限
                shopper_user_prem.set_shopper_perm(shopper_auth)
                # 登录
                login(request, shopper_auth)
                # 记录ip
                Ip.ip_.create(ips=ip, shopper=shopper_auth)
                # 删掉session中verification_code键值对
                del request.session['verification_code']
            except Exception as e:
                # 服务器错误
                logger.error('Login_error:{}'.format(str(e)))
                return JsonResponse(response_code.register_error)
            else:
                return JsonResponse(response_code.register_success)


class Verification_code(APIView):
    title = '拼夕夕商家注册'
    content = '亲爱的商家,【拼夕夕】欢迎您的加入,您的邀请码{code},有效期10分钟。'

    def post(self, request):
        """发送验证码"""
        email = request.data.get('email')
        # 获取随机6为验证码
        code = tasks.set_verification_code()
        try:
            User.objects.get(email=email)
            # 邮箱存在
            return JsonResponse(response_code.email_exist)
        except User.DoesNotExist:
            # 邮箱不存在可以
            self.content.format(code)
            try:
                # 异步发送验证码
                tasks.send_verification.delay(title=self.title, content=self.content, user_email=email)
                request.session['verification_code'] = code
                return JsonResponse(response_code.email_verification_success)
            except Exception as e:
                # 发送失败
                logger.error('send_email:{}'.format(str(e)))
                return JsonResponse(response_code.server_error)
