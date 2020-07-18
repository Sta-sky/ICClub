import pymysql
pymysql.version_info=(1,3,13,"final",0)
pymysql.install_as_MySQLdb()
#
# from activ.models import Activity
#
#
# #
# db = pymysql.connect(host='127.0.0.1', user='root', port=3306, password='123456',
#                      database='ICClubs', charset='utf8')
#
# cur = db.cursor()
#
# # static/images/旅游.jpeg
# #
# # static/images/跑步.jpeg
#
# # 活动点赞 收藏表    活动id,点赞数，收藏数
# activity_dis = [
#     (1,99,20),
#     (1,51,66),
#     (3,66,55),
#     (5,12,3),
#     (9,0,0)
# ]
#
#
#
# interest = [
#     ('旅游', 'static/images/travel.jpeg'),
#     ('跑步', 'static/images/run.jpeg'),
#     ('学习', 'static/images/study.jpeg')
# ]
#
# try:
#     ins = 'insert into interest_tag (interests,img_url,created_time,updated_time) values(%s,%s,now(),now())'
#     cur.executemany(ins, interest)
#     db.commit()
#     pass
#     # ins = "update interest_tag set img_url='static/images/run.jpeg' where interests='跑步'"
#     # cur.execute(ins)
#     # db.commit()
#     # ins = "update interest_tag set img_url='static/images/travel.jpeg' where interests='旅游'"
#     # cur.execute(ins)
#     # db.commit()
#
#     # inas = 'insert into activity_display (activity_id,likes,collection) values(%s,%s,%s)'
#     # cur.executemany(inas, activity_dis)
#     # db.commit()
#
# except Exception as e:
#     print('数据库写入失败，活动标签已存在！')
# else:
#     print('活动兴趣表已成功写入%s条数据' % len(interest))
# print('开始发布一个活动吧！')
#
# # username = UserRegist.objects.get(username='crazycode')
# # Activity.objects.create(user=username, tag=interest, subject=title, content=content,status=1)
#
#
# cur.close()
# db.close()
