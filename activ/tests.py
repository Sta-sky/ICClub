import random
import re
from urllib import parse

from django.test import TestCase

# Create your tests here.


# a = ['s','q','123','sdsd']
# b= [1,2,3,4]
# res = random.sample(a,1)
# # # print(a[100])
# print(res)
#
# a+=b
# print(a)


# print(random.randint(0,1))
# from django_redis import get_redis_connection
#
# class A:
#     def __init__(self):
#         pass
#
# a =A()
# r = get_redis_connection('newact')
# r.set(1,a)
# res = r.get(1)
# print(res)

# res = 'static/images/sadasdpkkj.jpg'
# image = re.findall(r'^.+[/\\](.+)(\..+)$', res)
# print(image)

# label = ''
# lab = parse.unquote(label)
# print(1)
# print(lab,1)

# data:image/jpeg;base64  data:image/jpeg;base64
# a = 'data:image/jpeg;base64'
# img = re.findall(r'^data:image/(.+?);base64', a)[0]
# print(img)


lists = [
    [1, 0.5, 0.8, 0, 0.2, 0.5],
    [1, 2, 1, 0, 0.22, 0.55],
    [1, 2, 3, 1, 2, 2.5],
    [0, 1, 0, 4, 2, 3.5],
    [0, 3, 0, 4, 5, 1],
    [0, 5, 0, 8, 2, 9],
]
result = []
for k,lis in enumerate(lists):
    line = k
    a = lis
    index = 0
    big = a[index]
    if line == 0:
        index = 1
        big = a[index]
    for i, j in enumerate(a):
        print(i, j)
        if i == line:
            print(i)
            continue
        if j > big:
            index = i
            big = j
    result.append((big,index))
print('***************')
print(result)

