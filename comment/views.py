import json

from django.http import JsonResponse
from django.views.generic.base import View
from comment.models import ActivityComment, AdminArticleComment
from tools.response_code import code
from tools.logging_checked import login_check


# Create your views here.
# 活动评论
class ActivityCommentView(View):

    def get(self, request):
        """
            get请求不判断登录，直接返回所有评论信息
        :param request:
        :return:
        """
        # print('这是GET请求====')
        # 获取活动id
        act_id = request.GET.get('act_id')
        act_id = int(act_id)
        print('活动ID', act_id, type(act_id))

        # 通过评论id，取出所有评论信息，将评论信息返回
        comment_list = ActivityComment.objects.filter(activity_id=act_id, review_id=0).order_by('comment_time')
        data = []
        for comment in comment_list:
            comment_info = {}
            comment_info['id'] = comment.id
            comment_info['user_id'] = comment.user_id
            comment_info['act_id'] = comment.activity_id
            comment_info['nickname'] = comment.user.userinfo.nickname
            comment_info['comment_time'] = str(comment.comment_time.strftime('%m-%d %H:%M:%S'))
            comment_info['comment_text'] = comment.comment_text
            review_data = []
            review_data = self.get_review(review_data, act_id, comment)
            # TODO 按评论时间排序（暂略）

            # 将回复信息列表放入对应评论字典
            comment_info['review'] = review_data
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
        # print("\033[36m已经入POST函数\033[0m")
        obj_data = request.body
        data = json.loads(obj_data)
        if not data:
            print('数据未提交成功')
            result = {'code': 10501, 'data': '数据提交错误'}
            return JsonResponse(result)
        # 获取活动id
        act_id = int(request.GET.get('act_id'))
        print('活动ID', act_id, type(act_id))
        # 获取评论用户id
        user_id = request.myuser.id
        username = request.myuser.username
        # print("用户ID：%s,用户名：%s" % (user_id, username))
        # 获取要回复用户的id
        re_user_id = data.get('re_user_id',0)
        re_user_id = int(re_user_id)
        if user_id == re_user_id:
            return JsonResponse({'code': 10502, 'data': '自言自语有什么意思，浪费内存……'})
        # 获取评论信息
        comment_text = data['comment_text'].strip()
        if not len(comment_text):
            return JsonResponse({'code': 10503, 'data': '评论内容为空'})
        review_id = data.get('review_id')
        # 将评论或回复写入数据库
        if not review_id:
            # print("这是评论")
            try:
                comment = ActivityComment.objects.create(user_id=user_id, activity_id=act_id, comment_text=comment_text)
            except Exception as e:
                print(e, '插入数据库异常')
                return JsonResponse(code[10001])
        else:
            # print("这是回复")
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
            comment_info = {}
            comment_info['id'] = comment.id
            comment_info['user_id'] = comment.user_id
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
        result = {'code': 201, 'data': data}
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
        review_list = ActivityComment.objects.filter(activity_id=act_id, review_id=comment.id).order_by('comment_time')
        if not review_list:
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
                self.get_review(review_data, act_id, review)
            return review_data

        pass

# 公告评论
class ArticleCommentView(View):

    def get(self, request):
        """
            get请求不判断登录，直接返回所有评论信息
        :param request:
        :return:
        """
        # print('这是GET请求====')
        # 获取活动id
        art_id = request.GET.get('art_id')
        art_id = int(art_id)
        print('活动ID', art_id, type(art_id))

        # 通过评论id，取出所有评论信息，将评论信息返回
        comment_list = AdminArticleComment.objects.filter(article_id=art_id, review_id=0).order_by('comment_time')
        data = []
        for comment in comment_list:
            comment_info = {}
            comment_info['id'] = comment.id
            comment_info['user_id'] = comment.user_id
            comment_info['act_id'] = comment.article_id
            comment_info['nickname'] = comment.user.userinfo.nickname
            comment_info['comment_time'] = str(comment.comment_time.strftime('%m-%d %H:%M:%S'))
            comment_info['comment_text'] = comment.comment_text
            review_data = []
            review_data = self.get_review(review_data, art_id, comment)
            # TODO 按评论时间排序（暂略）

            # 将回复信息列表放入对应评论字典
            comment_info['review'] = review_data
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
        # print("\033[36m已经入POST函数\033[0m")
        obj_data = request.body
        data = json.loads(obj_data)
        if not data:
            print('数据未提交成功')
            result = {'code': 10501, 'data': '数据提交错误'}
            return JsonResponse(result)
        # 获取活动id
        art_id = int(request.GET.get('art_id'))
        print('活动ID', art_id, type(art_id))
        # 获取评论用户id
        user_id = request.myuser.id
        username = request.myuser.username
        # print("用户ID：%s,用户名：%s" % (user_id, username))
        # 获取要回复用户的id
        re_user_id = data.get('re_user_id',0)
        re_user_id = int(re_user_id)
        if user_id == re_user_id:
            return JsonResponse({'code': 10502, 'data': '自言自语有什么意思，浪费内存……'})
        # 获取评论信息
        comment_text = data['comment_text'].strip()
        if not len(comment_text):
            return JsonResponse({'code': 10503, 'data': '评论内容为空'})
        review_id = data.get('review_id')
        # 将评论或回复写入数据库
        if not review_id:
            # print("这是评论")
            try:
                comment = AdminArticleComment.objects.create(user_id=user_id, article_id=art_id, comment_text=comment_text)
            except Exception as e:
                print(e, '插入数据库异常')
                return JsonResponse(code[10001])
        else:
            # print("这是回复")
            try:
                review = AdminArticleComment.objects.create(user_id=user_id, article_id=art_id, comment_text=comment_text,
                                                        review_id=review_id)
            except Exception as e:
                print(e, '插入数据库异常')
                return JsonResponse(code[10001])
        # 通过评论id，取出所有评论信息，将评论信息返回
        comment_list = AdminArticleComment.objects.filter(article_id=art_id, review_id=0).order_by('comment_time')
        data = []
        for comment in comment_list:
            comment_info = {}
            comment_info['id'] = comment.id
            comment_info['user_id'] = comment.user_id
            comment_info['act_id'] = comment.article_id
            comment_info['nickname'] = comment.user.userinfo.nickname
            comment_info['comment_time'] = str(comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'))
            comment_info['comment_text'] = comment.comment_text
            review_data = []
            review_data = self.get_review(review_data, art_id, comment)
            # 按评论时间排序（暂略）

            # 将回复信息列表放入对应评论字典
            comment_info['review'] = review_data
            data.append(comment_info)
        result = {'code': 201, 'data': data}
        # result = {'code': 201, 'data': '评论已提交保存'}
        return JsonResponse(result)
        pass

    def get_review(self, review_data, art_id, comment):
        """
            递归取评论回复，暂不考虑递归深度
        :param review_data:
        :param art_id:
        :param comment:
        :return:
        """
        review_list = AdminArticleComment.objects.filter(article_id=art_id, review_id=comment.id).order_by('comment_time')
        if not review_list:
            return review_data
        else:
            for review in review_list:
                review_info = {}
                review_info['id'] = review.id
                review_info['a_user_id'] = review.user_id
                review_info['b_user_id'] = AdminArticleComment.objects.filter(id=review.review_id)[0].user_id
                review_info['a_nickname'] = review.user.userinfo.nickname
                review_info['b_nickname'] = AdminArticleComment.objects.filter(id=review.review_id)[
                    0].user.userinfo.nickname
                review_info['review_time'] = str(review.comment_time.strftime('%m-%d %H:%M:%S'))
                review_info['review_text'] = review.comment_text
                review_data.append(review_info)
                self.get_review(review_data, art_id, review)
            return review_data

        pass