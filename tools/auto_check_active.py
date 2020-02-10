import json
from datetime import datetime
import threading
from threading import Timer
from django_redis import get_redis_connection
from activ.models import Activity

def auto_check():
    redis_conn = get_redis_connection('activity')
    redis_conn=json.dumps(redis_conn)
    keys = redis_conn.keys()
    for item in keys:
        data=redis_conn.get(item)

        active=Activity.objects.get(id=item)
        if len(data)>active.get('condition'):
            #TODO 给用户发邮件
            status=2
            Activity.objects.update(id=item,status=status)
        elif datetime.now()>active.get('end_time'):
            status=3
            Activity.objects.update(id=item,status=status)



timer = threading.Timer(24*3600, auto_check)
timer.start()

