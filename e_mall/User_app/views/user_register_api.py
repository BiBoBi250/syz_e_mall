from User_app.views import tasks
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from User_app.models.user_models import Consumer
from django.contrib.auth import login
from django.http import Http404, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .tasks import *
from e_mall.authentication_rewrite import Email_or_Username
from e_mall.response_code import *
import logging

logger = logging.getLogger('User_app')
# 用户日志错误记录
logging.basicConfig(filename='User_app/error.log',
                    level=logging.ERROR,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                    )

# 响应状态实例
response_code = Response_code()

# 认证实例
email_or_username = Email_or_Username()


class Login(APIView):
    def post(self, request):
        """消费者登录"""
        login_id = request.data.get('login_id')
        password = request.data.get('password')
        try:
            # 认证用户
            consumer = email_or_username.authenticate(request, login_id, password)
            if consumer:
                # 登录，发送session_id
                login(request, consumer)
                return JsonResponse(response_code.login_success)
            # 登录失败，密码或账号不正确
            return JsonResponse(response_code.login_error)
        except Exception as e:
            logger.error('login_error:{}'.format(str(e)))
            return JsonResponse(response_code.server_error)


class Register(APIView):
    def post(self, request):
        """消费者注册"""
        username = request.data.get('username')
        password = request.data.get('password')
        sex = request.data.get('sex')
        email = request.data.get('email')
        telephone = request.data.get('phone')
        verification_code = request.data.get('verification_code')  # 验证码
        try:
            User.objects.get(username=username)
            # 存在用户
            return JsonResponse(response_code.user_existed)
        except User.DoesNotExist:
            code_status = True if verification_code == request.session['verification_code'] else False
            if not code_status:
                return JsonResponse(response_code.verification_code_error)
        except Exception as e:
            # 服务器错误
            logger.error('Login_error:{}'.format(str(e)))
            return JsonResponse(response_code.register_error)
        # 额外参数
        try:
            extra_fields = {
                'is_staff': False,
                'is_superuser': False,
                'is_active': True
            }
            # 创建消费者
            consumer = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                **extra_fields,
                                                )
            # 创建消费者其他信息
            Consumer.consumer_.create(consumer=consumer, sex=sex, telephone=telephone)
            # 认证用户
            consumer = email_or_username.authenticate(request, username, password)
            # 登录
            login(request, consumer)
        except Exception as e:
            # 服务器错误
            logger.error('Login_error:{}'.format(str(e)))
            return JsonResponse(response_code.register_error)
        else:
            return JsonResponse(response_code.register_success)


class Verification_code(APIView):
    title = '拼夕夕用户注册'
    content = '亲爱的用户,【拼夕夕】商城欢迎您,您的邀请码{code},有效期10分钟。'

    def post(self, request):
        """发送验证码"""
        email = request.data.get('email')
        # 获取随机6为验证码
        code = tasks.set_verification_code()
        try:
            User.objects.get(email=email)
            # 邮箱存在
            return JsonResponse(response_code.email_verification_error)
        except User.DoesNotExist:
            # 邮箱不存在可以
            self.content.format(code)
            try:
                # 发送验证码
                tasks.send_verification.delay(title=self.title, content=self.content, user_email=email)
                request.session['verification_code'] = code
                return JsonResponse(response_code.email_verification_success)
            except Exception as e:
                # 发送失败
                logger.error('send_email:{}'.format(str(e)))
                return JsonResponse(response_code.server_error)
