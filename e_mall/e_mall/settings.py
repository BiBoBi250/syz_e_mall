"""
Django settings for e_mall project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ruu2)x=u+^l3mx27$(9)q1sk)(55t1csx%41-90nt%w8dw_(&i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Manager_app',  # 管理员app
    'Remark_app',   # 评论app
    'Shop_app',     # 商品app
    'Shopper_app',  # 店家app
    'User_app',     # 用户app
    'Order_app',    # 订单处理app
    'rest_framework',  # restful api
    'mdeditor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_mall.urls'


# AUTH_USER_MODEL = 'Manager_app.Manager_user'

# 加密算法，默认取第一个
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS':['vue_e_mall/dist'],  # 该目录是vue项目的名称
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'e_mall_db',  # 数据库名
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'syzxss247179876'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# 语言
LANGUAGES = [
    ('zh-Hans', 'Chinese'),
    ('en-us','English')
]

# 编码
LANGUAGE_CODE = 'zh-Hans'
# LANGUAGES_CODE = 'en-us'
# 时区
TIME_ZONE = 'Asia/Shanghai'

# 本地翻译文件路径
LOCALE_PATHS = (
    os.path.join(BASE_DIR,'locale'),
)
# 国际化
USE_I18N = True

# 本地化
USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 静态文件路由
STATIC_URL = '/static/'

# 静态文件
STATICFILES_DIRS = [
    # 替换反斜杠
    os.path.join(BASE_DIR, 'vue_e_mall/dist/static').replace('\\', '/')
]

# STATIC_ROOT 用于部署时候将静态文件全部集中存放,根目录从盘区开始，所以尽量使用绝对路径
# STATIC_ROOT = 'd:/syz/virtualenvs/e_mall/e_mall/nginx/static/'

# 缓存
CACHES = {
    'default':
        {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://:syzxss247179876@127.0.0.1:6379/3',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
}

# 图片等媒体文件的url
MEDIA_URL = '/media/'  # 方便url使用的目录，与项目中的目录名不一样,同时也用于数据库存储的路径,要加上/来结尾

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 用户上传的文件目录

# 重写User表
# AUTH_USER_MODEL = 'Manager_app.Manager_user'

# 会话session设置
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）

SESSION_COOKIE_NAME = "e_mall_sessionid"

# Session的cookie保存在浏览器上时的key，session根据此key来生成，如果不支持cookie，那么也就不支持session
# 浏览器关闭之后清除的是cookie所保存的服务器传下来的sessionid，而不是session，一旦请求头中的sessionid匹配不上服务器中的sessionid，则请求失败。
# 当session过期后，服务器才会传递一个新的session

SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径（默认）

SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）

SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）

SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）

SESSION_COOKIE_AGE = 60 * 24 * 60  # Session的cookie失效日期（30min）（默认），和SESSION_EXPIRE_AT_BROWSER_CLOSE二选一

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期（默认）

SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存


# 首页跳转地址
SIMPLEUI_INDEX = '/'

# 设置后台logo
SIMPLEUI_LOGO = 'https://django-blog-syz.oss-cn-shanghai.aliyuncs.com/login.jpg'

# 隐藏服务器信息
SIMPLEUI_HOME_INFO = False

# 隐藏最近动作
SIMPLEUI_HOME_ACTION = True

# 创建自定义菜单
'''

SIMPLEUI_CONFIG = {
    'system_keep':False,
    'menu_display':['订单管理','库存管理','卖家评论','信誉查看','店铺管理','商品管理','个人信息'],
    'dynamic': False,
    'menus': [{
        'name': '订单管理',
        'icon': 'fa fa-hand-peace-o',
        'models': [{
            'name': '一个月内的订单记录',
            'icon': 'fa fa-line-chart',
            'url': '/admin/'
        }]
    }, {
        'name': '库存管理',
        'icon': 'fa fa-truck',
        'url': '/admin/',
    }, {
        'name': '卖家评论',
        'icon': 'fa fa-handshake-o',
        'models': [{
            'name': '回复管理',
            'url': '/admin/',
            'icon': 'fa fa-handshake-o'
        }]
    }, {
        'name': '信誉查看',
        'icon': 'fa fa-diamond',
        'url': '/admin',
    }, {
        'name': '店铺管理',
        'icon': 'fa fa-database',
        'url':'/admin/',
    },{
        'name': '商品管理',
        'icon': 'fa fa-suitcase',
        'url':'/admin/',
    }, {
        'name': '个人信息',
        'icon': 'fa fa-user-o',
        'models': [{
            'name': '修改资料',
            'url': '/admin/',
            'icon': 'fa fa-id-card-o'
        }, {
            'name': '密码修改',
            'icon': 'fa fa-id-card-o',
            'url': '/admin/'
        }]
    }]
}

'''