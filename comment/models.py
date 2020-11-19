from django.db import models

# Create your models here.
from activitys.models import Activity, AdminArticle
from users.models import UserRegist


class ActivityComment(models.Model):
    # 评论表

    # 评论id，作为主键，comment_id=
    activity = models.ForeignKey(Activity, verbose_name='所属活动')
    user = models.ForeignKey(UserRegist, verbose_name='评论/回复人')
    comment_text = models.CharField(max_length=320, verbose_name='评论内容')
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    review_id = models.IntegerField(default=0, verbose_name='被回复的评论id')

    class Meta:
        db_table = 'activity_comment'
        verbose_name_plural = '活动评论'

    def __str__(self):
        return 'id:%s,活动id:%s,用户id：%s,回复id:%s,时间：%s' % (
        self.id, self.activity_id, self.user_id, self.review_id, self.comment_time)


class AdminArticleComment(models.Model):
    # 评论表

    # 评论id，作为主键，comment_id=
    article = models.ForeignKey(AdminArticle, verbose_name='所属文章')
    user = models.ForeignKey(UserRegist, verbose_name='评论/回复人')
    comment_text = models.CharField(max_length=320, verbose_name='评论内容')
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    review_id = models.IntegerField(default=0, verbose_name='被回复的评论id')

    class Meta:
        db_table = 'article_comment'
        verbose_name_plural = '公告文章评论'

    def __str__(self):
        return 'id:%s,活动id:%s,用户id：%s,回复id:%s,时间：%s' % (
        self.id, self.article_id, self.user_id, self.review_id, self.comment_time)
