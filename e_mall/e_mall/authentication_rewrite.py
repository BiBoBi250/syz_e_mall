from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class Email_or_Username(ModelBackend):
    def authenticate(self,request,username=None,password=None, **kwargs):
        """认证商家，允许商家用户名或邮箱登录"""
        try:
            shopper = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None
        else:
            if shopper.check_password(password):
                return shopper
            return None
