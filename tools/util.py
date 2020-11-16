import os
import json
import datetime
from ICClub import settings


# json序列化工具   解决某些日期格式json转换不成功
class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')
        
        
def format_str(source_str):
    parse_str = source_str.strip().replace(' ', '').\
        replace('\t', ' ').replace('\r', '').replace('\n', '')
    return parse_str


def upload_img_save(img_data, img_save_path):
    file_path = os.path.realpath(settings.BASE_DIR + '/ICClub/static/' + img_save_path)
    print('文件保存路径')
    print(file_path)
    try:
        with open(file_path, 'wb') as fp:
            fp.write(img_data)
        return {'code': 30000, 'message': f'图片保存成功'}
    except Exception as e:
        return {'code': 30001, 'message': f'图片保存异常，原因为{e}'}
    