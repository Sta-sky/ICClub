import json

from django.http import JsonResponse
from django.test import TestCase

# Create your tests here.
from django.views.generic.base import View

from comment.models import ActivityComment
from response_code import code
from tools.logging_checked import login_check


class ActivityCommentView(View):

    def get(self, request):
        """
            get请求不判断登录，直接返回所有评论信息
        :param request:
        :return:
        """
        print('这是GET请求====')
        # 获取活动id
        act_id = request.GET.get('act_id')
        act_id = int(act_id)
        print('活动ID', act_id, type(act_id))

        # 通过评论id，取出所有评论信息，将评论信息返回
        comment_list = ActivityComment.objects.filter(activity_id=act_id, review_id=0).order_by('comment_time')
        data = []
        for comment in comment_list:
            # print("\033[31m这是测试专用字段1\033[0")

            comment_info = {}
            comment_info['id'] = comment.id
            comment_info['user_id'] = comment.user_id
            # print("\033[31m这是测试专用字段2\033[0", comment_info['user_id'])

            comment_info['act_id'] = comment.activity_id
            comment_info['nickname'] = comment.user.userinfo.nickname
            comment_info['comment_time'] = str(comment.comment_time.strftime('%m-%d %H:%M:%S'))
            comment_info['comment_text'] = comment.comment_text
            review_data = []
            review_data = self.get_review(review_data, act_id, comment)
            # 按评论时间排序（暂略）

            # 将回复信息列表放入对应评论字典
            comment_info['review'] = review_data
            # print("\033[31m这是测试专用字段8=================\033[0")
            # print("\033[36m回复内容：\033[0m", comment_info['review'])
            data.append(comment_info)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)

        pass

    @login_check
    def post(self, request):
        """
            检查用户登录，确认登录。提交评论，评论存数据库，返回评论信息
        :param request:
        :return:
        print('这是POST请求')
        """
        print("\033[36m已经入POST函数\033[0m")
        obj_data = request.body
        data = json.loads(obj_data)
        if not data:
            print('数据未提交成功')
            result = {'code': 10501, 'data': '数据提交错误'}
            return JsonResponse(result)
        print('============================')
        # 获取活动id
        act_id = int(request.GET.get('act_id'))
        print('活动ID', act_id, type(act_id))
        # 获取评论用户id
        user_id = request.myuser.id
        username = request.myuser.username
        print("用户ID：%s,用户名：%s" % (user_id, username))
        print('============================')
        # 获取要回复用户的id
        re_user_id = data.get('re_user_id',0)
        re_user_id = int(re_user_id)
        print("\033[36m要回复的ID：%s\033[0m" % re_user_id,type(re_user_id))
        if user_id == re_user_id:
            return JsonResponse({'code': 10502, 'data': '自言自语有什么意思，浪费内存……'})
        # 获取评论信息
        comment_text = data['comment_text'].strip()
        print("\033[36m评论内容：\033[0m", comment_text)
        if not len(comment_text):
            return JsonResponse({'code': 10503, 'data': '评论内容为空'})
        review_id = data.get('review_id')
        print("\033[36m回复ID\033[0m", review_id)
        # 将评论或回复写入数据库
        if not review_id:
            print("这是评论")
            try:
                comment = ActivityComment.objects.create(user_id=user_id, activity_id=act_id, comment_text=comment_text)
            except Exception as e:
                print(e, '插入数据库异常')
                return JsonResponse(code[10001])
        else:
            print("这是回复")
            try:
                review = ActivityComment.objects.create(user_id=user_id, activity_id=act_id, comment_text=comment_text,
                                                        review_id=review_id)
            except Exception as e:
                print(e, '插入数据库异常')
                return JsonResponse(code[10001])
        # 通过评论id，取出所有评论信息，将评论信息返回
        comment_list = ActivityComment.objects.filter(activity_id=act_id, review_id=0).order_by('comment_time')
        data = []
        for comment in comment_list:
            print("\033[36m这是测试专用字段1\033[0")

            comment_info = {}
            comment_info['id'] = comment.id
            comment_info['user_id'] = comment.user_id
            print("\033[36m这是测试专用字段2\033[0", comment_info['user_id'])

            comment_info['act_id'] = comment.activity_id
            comment_info['nickname'] = comment.user.userinfo.nickname
            comment_info['comment_time'] = str(comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'))
            comment_info['comment_text'] = comment.comment_text
            review_data = []
            review_data = self.get_review(review_data, act_id, comment)
            # 按评论时间排序（暂略）

            # 将回复信息列表放入对应评论字典
            comment_info['review'] = review_data
            data.append(comment_info)
        print("\033[36m这是测试专用字段8\033[0")
        result = {'code': 201, 'data': data}
        print('\033[36m评论已存表\033[0m')
        # result = {'code': 201, 'data': '评论已提交保存'}
        return JsonResponse(result)
        pass

    def get_review(self, review_data, act_id, comment):
        """
            递归取评论回复，暂不考虑递归深度
        :param review_data:
        :param act_id:
        :param comment:
        :return:
        """
        # print("\033[36m评论ID：\033[0m", comment.id)
        review_list = ActivityComment.objects.filter(activity_id=act_id, review_id=comment.id).order_by('comment_time')
        # print("\033[36m review_list：review_list\033[0m", review_list)
        if not review_list:
            # print("\033[36m这是测试专用字段+++++++++++++++++++++++\033[0")
            # print("review_data长度", len(review_data))
            return review_data
        else:
            for review in review_list:
                review_info = {}
                review_info['id'] = review.id
                review_info['a_user_id'] = review.user_id
                review_info['b_user_id'] = ActivityComment.objects.filter(id=review.review_id)[0].user_id
                review_info['a_nickname'] = review.user.userinfo.nickname
                review_info['b_nickname'] = ActivityComment.objects.filter(id=review.review_id)[
                    0].user.userinfo.nickname
                review_info['review_time'] = str(review.comment_time.strftime('%m-%d %H:%M:%S'))
                review_info['review_text'] = review.comment_text
                review_data.append(review_info)
                # print("\033[36m review_info\033[0m", review_info)
                # print("\033[36m review_data\033[0m", review_data)
                self.get_review(review_data, act_id, review)
            return review_data

        pass
