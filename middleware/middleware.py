from django.utils.deprecation import MiddlewareMixin
from django.http import Http404


class Mymiddle(MiddlewareMixin):
    import time
    dic = {}
    dic['time'] = time.time()  # 用于记录这次单次请求的起始时间

    def process_request(self, request):
        id = request.META['REMOTE_ADDR']
        import time
        self.dic.get(id, 0)
        self.first_time = time.time()
        if time.time() - self.dic['time'] > 10:  # 如果禁止时间超出了10s 就解除禁止
            self.dic[id] = 0

    def process_response(self, request, response):
        import re
        import time
        target_time = time.time() - self.dic['time']
        environment = request.environ
        # print(environment)
        target = environment['HTTP_USER_AGENT']
        # print(target)
        id = request.META['REMOTE_ADDR']
        re_result = re.findall(r'^Mozilla/|^S', target, re.S | re.M)
        num = self.dic.get(id, 0)
        if num < 10:  # 判断单秒内是否超过10次访问
            if re_result:
                if target_time <= 1:  # 单击时间小于１秒
                    self.dic[id] = num + 1
                    return response

                else:
                    self.dic[id] = 0  # 单击时间大于１秒,重新记０
                    self.dic['time'] = self.first_time
                    return response
            else:
                return Http404
        return Http404

# class Mymiddle(MiddlewareMixin):
#     """
#         此中间件限制一个IP地址对应的访问的次数不能超过10次,超过后限制使用5分钟
#     """
#     visit_times = {}#visit_times = {'ip':'num',time:''}
#     # TODO 此字典用于记录客户端IP地址有访问次数 后期建议改为redis
#     def process_request(self, request):
#         ip_address = request.META['REMOTE_ADDR']
#         # 得到IP地址
#         # if not re.match('^/test',request.path_info):
#         #     return
#         times = self.visit_times.get(ip_address, 0)
#         print("IP:", ip_address, '已经访问过', times, '次!:')
#         self.visit_times[ip_address] = times + 1
#         # TODO 测试时关闭此功能
#         # if times < 5:
#         #     return
#         # return JsonResponse(code[10201])
#         return


# class Mymiddle(MiddlewareMixin):
#     def process_request(self, request):
#         # IP = request.m
#
#         print("中间件方法 process_request 被调用")
#
#     def process_view(self, request, callback, callback_args, callback_kwargs):
#         print("中间件方法 process_view 被调用")
#
#     def process_response(self, request,response):
#         print("中间件方法 process_response 被调用")
#         return response
