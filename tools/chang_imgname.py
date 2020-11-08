from urllib import parse


def parse_imgname(img):
    list_url = img.split('/')
    list_left = img.split('/')[0:len(list_url) - 1]
    img_name = list_url[-1].split('.')
    new_name = parse.quote(img_name[0]) + '.' + img_name[1]
    list_left.append(new_name)
    result = '/'.join(list_left)
    return result


import re

# 看看这个 写好了
imageurl = 'static/images/跑步.jpeg'
image = re.findall(r'^.+[/\\](.+)\..+$', imageurl)[0]

