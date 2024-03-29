import os

SERIP127 = '127.0.0.1'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6_ehqzashtw_a=ab#92y+z#w+1rkb)7yoxwz0u#q2$6)9x6x^l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 数据库字段时间告警消除设置DateTimeField
USE_TZ = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',  # 请保持channels在第一项
    'corsheaders',
    'ICClub',
    'activitys',
    'users',
    'community',
    'comment',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.middleware.Mymiddle',
]

ROOT_URLCONF = 'ICClub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'media'),
                 os.path.join(BASE_DIR, 'ICClub/templates'),
                 ],
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

WSGI_APPLICATION = 'ICClub.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ICClub',
        # 'HOST': SERIP,
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PORT': '3306',
        'PASSWORD': '123456',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True



STATIC_URL = '/static/'
STATICFILE_DIRS = (
    os.path.join(BASE_DIR, 'media')
)

# token key
JWT_TOKEN_KEY = 'dangyuanyang'

# auth微博授权
WEIBO_CLIENT_ID = '195501655'
WEIBO_CLIENT_SECRET = 'da9024403990743e34536e05dbe451ab'
WEIBO_REDIRECT_URI = 'http://' + SERIP127 + ':8000/user/bind'

# 跨域配置
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
# 跨域白名单  ，凡是出现在白名单中的域名，都可以访问后端接口
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',
    'http://localhost:8000',
)

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:7000'
]

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
    'X-Frame-Options'
)

# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 固定写法
EMAIL_HOST = 'smtp.qq.com'  # 腾讯QQ邮箱 SMTP 服务器地址
EMAIL_PORT = 25  # SMTP服务的端口号
EMAIL_HOST_USER = '1361704733@qq.com'
EMAIL_HOST_PASSWORD = 'mcaktiumxqlufhfh'  # 在QQ邮箱->设置->帐户->“POP3/IMAP......服务” 里得到的在第三方登录QQ邮箱授权码
EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)默认false  True
SERVER_EMAIL = '1361704733@qq.com'
ADMINS = [('superman', '1361704733@qq.com'), ]
APPEND_SLASH = False

# 系统邮件地址
SYSEMAIL = '1361704733@qq.com'
DJREIDS_IP = 'redis://@' + SERIP127 + ':6379/'

# 用户找回密码、激活邮件的邮箱验证地址
EMAIL_URL = 'http://' + SERIP127 + ':7000/templates/email_activ.html?code={}'


# django_redis缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': DJREIDS_IP + '9',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'user': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': DJREIDS_IP + '10',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'users': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": DJREIDS_IP + '11',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"

        }
    },
    'activitys': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': DJREIDS_IP + '12',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'newact': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': DJREIDS_IP + '13',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}


# 一旦启用，通道将自己集成到Django中并控制runserver命令
ASGI_APPLICATION = "ICClub.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1',6379),],
        },
    },
}



# celery 工作区、回调区的redis配置
CELERY_BROKEN = '14'
CELERY_BACKEND = '15'


# websocket 配置
WEBSOCKET_ACCEPT_ALL = True


# 配置 MEDIA_ROOT 作为你上传文件在服务器中的基本路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'ICClub\\static\\') # 注意此处不要写成列表或元组的形式

# 上传图片文件夹  上传云端换第一个
IMGBATH = os.path.join(BASE_DIR, 'ICClub/static/')

# 标签图片路径
DBLABIMG = 'images/label/'

# 用户上传的活动图片
DBACTIMG = 'images/activity/'



# 官方活动图片
DBOFFIMG = 'images/official/'
OFFICAIAL_DIR = IMGBATH + DBOFFIMG


# 用户头像上传路径
DBUSEIMG = 'images/user_head/'
USERIMAGE_DIR = IMGBATH + DBUSEIMG

# 上传到后端所有图片后缀
IMG_END = '.jpg'

# 活动统计个数
ACTIVITY_NUM = 0

# 达成条件的活动
ACTCONDITION = []


