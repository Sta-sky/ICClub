import os
from celery import Celery
from ICClub import settings

# 为celery设置环境变量

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ICClub.settings'

# 配置  celery的中间键
broken = 'redis://@' + settings.SERIP127 + ':6379/' + settings.CELERY_BROKEN
backend = 'redis://@' + settings.SERIP127 + ':6379/' + settings.CELERY_BACKEND
# 初始化celery
app = Celery('ICClub', broker=broken, backend=backend)

# 加载项目配置文件
app.config_from_object('ICClub.settings')

# 注册celery任务队列
app.autodiscover_tasks(['celery_tasks'])
