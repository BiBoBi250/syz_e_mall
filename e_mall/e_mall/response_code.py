"""
自定义业务逻辑Code
"""

# 验证码验证成功
VERIFICATION_CODE_SUCCESS = 1

# 验证码验证失败
VERIFICATION_CODE_ERROR = 0

# 登录验证成功
LOGIN_VERIFICATION_SUCCESS = 11

# 登录验证失败
LOGIN_VERIFICATION_ERROR = -10

# 注册验证成功
REGISTER_VERIFICATION_SUCCESS = 21

# 注册验证失败
REGISTER_VERIFICATION_ERROR = -20

# 邮件验证成功
EMAIL_VERIFICATION_SUCCESS = 31

# 邮件验证失败
EMAIL_VERIFICATION_ERROR = -30

# 电话验证成功
PHONE_VERIFICATION_SUCCESS = 41

# 电话验证失败
PHONE_VERIFICATION_ERROR = -40

# 找回密码验证成功
FIND_PASSWORD_VERIFICATION_SUCCESS = 51

# 找回密码验证失败
FIND_PASSWORD_VERIFICATION_ERROR =-50

# 修改密码验证成功
MODIFY_PASSWORD_VERIFICATION_SUCCESS = 61

# 修改密码验证失败
MODIFY_PASSWORD_VERIFICATION_ERROR = -60

# 用户已经存在
USER_EXISTS = 7

# 用户不存在
USER_NOT_EXISTS = -7

# 邮箱已存在
EMAIL_EXISTS = 8

# 服务器无响应
SERVER_ERROR = 500


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

    @property
    def user_not_existed(self):
        """用户不存在"""
        self.result.update(dict(code=USER_NOT_EXISTS,msg='login',status='error'))
        return self.result
    @property
    def email_exist(self):
        """邮箱已存在"""
        self.result.update(dict(code=EMAIL_EXISTS, msg='email_verification', status='error'))
        return self.result
    @property
    def server_error(self):
        """服务器无响应"""
        self.result.update(dict(code=SERVER_ERROR, msg='server_error', status='error'))
        return self.result

