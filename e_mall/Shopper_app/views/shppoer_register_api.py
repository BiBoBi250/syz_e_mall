
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Permission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Shopper_app.models.shopper_models import Shoppers, Store, Ip
from django.http import Http404,JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from ..views import tasks
from e_mall.response_code import *
import logging

logger = logging.getLogger('shopper_app')  # 设置日志名
logging.basicConfig(filename='Shopper_app/error.log',
                    level=logging.ERROR,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                    ) # 日志文件


class Response_code:
    result = {
        'code': '',
        'msg': '',
        'status': '',
        'data': '',
    }
    @property
    def verification_code_error(self):
        """验证码验证"""
        self.result.update(dict(code=VERIFICATION_CODE_ERROR, msg='code',status='error'))
        return self.result
    @property
    def login_success(self):
        """登录验证成功"""
        self.result.update(dict(code=LOGIN_VERIFICATION_SUCCESS, msg='login', status='success'))
        return self.result

    @property
    def login_error(self):
        """登录验证失败"""
        self.result.update(dict(code=LOGIN_VERIFICATION_ERROR, msg='login', status='error'))
        return self.result

    @property
    def register_success(self):
        """注册验证成功"""
        self.result.update(dict(code=REGISTER_VERIFICATION_SUCCESS, msg='register', status='success'))
        return self.result

    @property
    def register_error(self):
        """注册验证失败"""
        self.result.update(dict(code=REGISTER_VERIFICATION_ERROR,msg='register',status='error'))
        return self.result

    @property
    def email_verification_success(self):
        """邮件验证成功"""
        self.result.update(dict(code=EMAIL_VERIFICATION_SUCCESS,msg='email_verification',status='success'))
        return self.result

    @property
    def email_verification_error(self):
        """邮件验证失败"""
        self.result.update(dict(code=EMAIL_VERIFICATION_ERROR,msg='email_verification',status='error'))
        return self.result

    @property
    def phone_verification_success(self):
        """手机验证成功"""
        self.result.update(dict(code=PHONE_VERIFICATION_SUCCESS,msg='phone_verification',status='success'))
        return self.result

    @property
    def phone_verification_error(self):
        """手机验证失败"""
        self.result.update(dict(code=PHONE_VERIFICATION_SUCCESS,msg='phone_verification',status='error'))
        return self.result

    @property
    def find_password_verification_success(self):
        """找回密码验证成功"""
        self.result.update(dict(code=FIND_PASSWORD_VERIFICATION_SUCCESS,msg='find_password',status='success'))
        return self.result

    @property
    def find_password_verification_error(self):
        """找回密码验证成功"""
        self.result.update(dict(code=FIND_PASSWORD_VERIFICATION_ERROR, msg='find_password', status='error'))
        return self.result

    @property
    def modify_password_verification_success(self):
        """找回密码验证成功"""
        self.result.update(dict(code=MODIFY_PASSWORD_VERIFICATION_SUCCESS, msg='modify_password', status='success'))
        return self.result

    @property
    def modify_password_verification_error(self):
        """找回密码验证成功"""
        self.result.update(dict(code=MODIFY_PASSWORD_VERIFICATION_ERROR, msg='modify_password', status='error'))
        return self.result

    @property
    def user_existed(self):
        """用户已经存在"""
        self.result.update(dict(code=USER_EXISTS, msg='register', status='error'))
        return self.result



class Shopper_user_prem:

    """设置权限"""
    permissions_pub = [
        '',
    ]

    def set_shopper_perm(self,user):
        permissions = Permission.objects.filter(codename__in=self.permissions_pub)
        for permission in permissions:
            # 增加商家基本权限
            user.user_permissions.add(permission)

class Login(APIView):
    def post(self,request):
        """登录"""
        ip = request.META.get('REMOTE_ADDR','unknown')
        username = request.data.get('username')
        password = request.data.get('password')
        response_code = Response_code()
        # 认证用户
        try:
           user_auth = authenticate(request,username=username,password=password)
           user_status = True if user_auth else False
           if user_status:
               # 登录，传输session_id
               login(request,user_auth)
               Ip.ip_.create(ips=ip,shopper=user_auth)
               return JsonResponse(response_code.login_success)
           else:
               # 登录失败
               return JsonResponse(response_code.login_error)
        except Exception as e:
            # 将错误写进日志
            logger.error('login_error:{}'.format(str(e)))
            return JsonResponse(response_code.login_error)


class Register(APIView):
    def post(self,request):
        """注册"""
        ip = request.META.get('REMOTE_ADDR','unknown') # 获取ip地址
        username = request.data.get('username').strip()
        password = request.data.get('password').strip()
        email = request.data.get('email').strip()
        telephone = request.data.get('phone').strip()
        sex = request.data.get('sex').strip()
        verification_code = request.data.get('verification_code').strip() # 验证码
        telephone = telephone
        # 响应状态实例
        response_code = Response_code()
        # 商家基本权限
        shopper_user_prem = Shopper_user_prem()
        try:
            User.objects.get(username=username)
        except:
            # 可以注册
            exists = False
            code_status = True if verification_code == request.session['verification_code'] else False
            if not code_status:
                return JsonResponse(response_code.verification_code_error)
        else:
            # 存在用户
            # 返回Json格式字符串
            return JsonResponse(response_code.user_existed)
        if not exists:
            # 额外参数
            extra_fields = {
                'is_staff':True,
                'is_superuser':False,
                'is_active':True
            }
            # 创建商家
            user = User.objects.create_user(username=username,email=email,password=password,
                                     **extra_fields)
            # 创建商家其他信息
            Shoppers.shoppers_.create(shopper=user,telephone=telephone,sex=sex)
            # 为每一个商家创建一个店铺
            Store.store_.create(shopper=user)
            # 认证用户
            user_auth = authenticate(request,usernam=username,password=password)
            # 设置权限
            shopper_user_prem.set_shopper_perm(user)
            # 登录
            login(request,user_auth)
            # 记录ip
            Ip.ip_.create(ips=ip,shopper=user_auth)
            # 删掉session中verification_code键值对
            del request.session['verification_code']
            return JsonResponse(response_code.register_success)


class Verification_code(APIView):
    title = '拼夕夕注册'
    content = '【拼夕夕】欢迎您的加入，您的邀请码{code},有效期10分钟。'

    def post(self,request):
        """发送验证码"""
        email = request.data.get('email')
        # 获取随机6为验证码
        code = tasks.set_verification_code()
        # 响应状态实例
        response_code = Response_code()
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
                return JsonResponse(response_code.email_verification_error)





























