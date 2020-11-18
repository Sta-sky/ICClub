import json
import datetime
import jwt
from ICClub import settings
from ICClub.settings import JWT_TOKEN_KEY


# json序列化工具   解决某些日期格式json转换不成功
from tools.response_code import code


class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')
        
        
def format_str(source_str):
    parse_str = source_str.strip().replace(' ', '').\
        replace('\t', ' ').replace('\r', '').replace('\n', '')
    return parse_str


def upload_img_save(img_data, img_save_path):
    file_path = settings.ACTIMAGE_DIR + img_save_path
    try:
        with open(file_path, 'wb') as fp:
            fp.write(img_data)
        return code[10500]
    except Exception as e:
        code[10501]['message'] = e
        return code
    
def judge_token_expire(token):
    try:
        res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
        return res
    except Exception as e:
        print(e)
        return None
    
    
    