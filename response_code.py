# 活动10000起

# 用户10100起

# 异常10200起


# 响应码 不要把响应码加 ""
# TODO 调用时导入 from response_code import code
# TODO 调用方法  code[200]
code = {
    200: {'code': 200, 'message': 'ok'},
    201: {'code': 201, "message": '请求正在处理'},
    202: {'code': 202, 'message': '用户已投票，请勿重复提交'},
    10000: {'code': 10000, 'message': 'Can not be empty!'},  # 不能为空
    10001: {'code': 10001, 'message': 'Create failure'},  # 插入数据库失败 创建失败
    10002: {'code': 10002, 'message': '查询内容异常'},    # 查询数据异常
    10003: {'code': 10003, 'message': ''},
    10004: {'code': 10004, 'message': '没有有效参数'},
    10005: {'cdoe': 10005, 'message': 'redis写入失败'},
    10006: {'code': 10006, 'message': '未定义标签,查询失败'},       #
    10200: {'code': 10200, 'message': 'token查询异常'},   # token
    10201: {'code': 10201, 'message': 'IP访问限制'},     # IP访问次数过多 ,限制5分钟
    10202: {'code': 10202, 'message': '非法访问'},      # 非法访问
    10203: {'code': 10203, 'message': '用户未登录'},
    10204: {'code': 10204, 'message': 'token认证过期。'},
    30000: {'code': 30000, 'message': '图片保存成功'},
    30001: {'code': 30001, 'message': '图片保存异常'},
    30002: {'code': 30002, 'message': '图片上传写入失败，请重新上传'}
}
