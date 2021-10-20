import json
import jwt
import hashlib
import datetime
from ICClub import settings
from django.http import JsonResponse
from ICClub.settings import JWT_TOKEN_KEY


# json序列化工具   解决某些日期格式json转换不成功
from tools.response_code import code


class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')
        
        
def format_str(source_str):
    return source_str.strip().replace(' ', '').\
        replace('\t', ' ').replace('\r', '').replace('\n', '')


def upload_img_save(img_data, img_save_path):
    file_path = settings.IMGBATH + img_save_path
    print('尽力啊了 文件保存路径为',file_path)
    try:
        with open(file_path, 'wb') as fp:
            fp.write(img_data)
        print('图片写入成功')
        return code[10500]
    except Exception as e:
        print(e)
        print('--------------------')
        code[10501]['message'] = e
        return code
    
def judge_token_expire(token):
    try:
        return jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
    except Exception as e:
        print(e)
        return None

    
def decode_md5(passwd):
    """ 密码解密 """
    try:
        m = hashlib.md5()
        m.update(passwd.encode())
        return m.hexdigest()
    except Exception as e:
        return False

# redis 用户注册登录短信验证码校验
def verify_sms_code(redis_obj, username, phone, user_code):
    try:
        # 取出code核对
        redis_code = redis_obj.hget(username, phone)
        redis_code = json.loads(redis_code)
    except Exception as e:
        return JsonResponse(code[10215])
    if user_code != redis_code:
        return JsonResponse(code[10216])
    # 验证完成删除
    redis_obj.hdel(username, phone)
    return False
    
    