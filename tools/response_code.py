"""
活动相关        10000
用户相关        10200
评论相关        10300
论坛相关        10400
工具相关        10500

TODO 200 响应码 默认为所有正常请求返回结果， 可自定义 message
"""


code = {
    200: {'code': 200, 'message': '成功', 'data': ''},

    10000: {'code': 10000, 'message': 'Can not be empty!'},  # 不能为空
    10001: {'code': 10001, 'message': 'Create failure'},  # 插入数据库失败 创建失败
    10002: {'code': 10002, 'message': '查询内容异常'},    # 查询数据异常
    10003: {'code': 10003, 'message': '活动未找到'},
    10004: {'code': 10004, 'message': '没有有效参数'},
    10005: {'cdoe': 10005, 'message': 'redis写入失败'},
    10006: {'code': 10006, 'message': '未定义标签,查询失败'},
    10007: {'code': 10007, "message": '请求正在处理'},
    10008: {'code': 10008, 'message': '用户已投票，请勿重复提交'},
    10009: {'code': 10009, 'message': '管理员数据请求失败，原因为：'},
    10010: {'code': 10010, 'message': '没有检索到关键字'},
    10011: {'code': 10010, 'message': '搜索的form表单查询数据错误'},
    10012: {'code': 10012, 'message': '⻚数有误,小于0或者大于总⻚数'},
    

    10200: {'code': 10200, 'message': 'token查询异常'},   # token
    10201: {'code': 10201, 'message': 'token已过期，请重新登录'},
    10203: {'code': 10203, 'message': '用户未登录, 请先登录'},
    10204: {'code': 10204, 'message': 'token认证过期。'},
    10205: {'code': 10205, 'message': '用户不存在'},
    10206: {'code': 10206, 'message': '你无权查看该页面'},
    10207: {'code': 10207, 'message': '用户信息修改自定义返回值'},
    10208: {'code': 10208, 'message': '自定义登录返回错误信息'},
    10209: {'code': 10209, 'message': '传入数据为空'},
    10210: {'code': 10209, 'message': '用户查询失败'},
    10211: {'code': 10209, 'message': '用户已经存在'},
    
    
    
    10500: {'code': 10500, 'message': '图片保存成功'},
    10501: {'code': 10501, 'message': '图片保存异常'},
    10502: {'code': 10502, 'message': '图片上传写入失败，请重新上传'},
    
    10505: {'code': 10505, 'message': 'IP访问限制'},# IP访问次数过多 ,限制5分钟
    10506: {'code': 10202, 'message': '请求方式错误'},  # 非法访问
}
