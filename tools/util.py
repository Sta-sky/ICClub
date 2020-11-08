import datetime
import json


# json序列化工具   解决某些日期格式json转换不成功
class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')