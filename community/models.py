from django.db import models
from activitys.models import UserInfo

class CommnuityLable(models.Model):
	lable_name = models.CharField(max_length=20, verbose_name='论坛标签名')
	img_url = models.ImageField(blank=True, verbose_name='标签默认图片')

	class Mete:
		db_table = 'commnuity_lable'

	def __str__(self):
		return 'id:%s lable_name:%s img_url:%s' % (self.id, self.lable_name, self.img_url)

class Commnuity(models.Model):
	commnuity_user = models.ForeignKey(UserInfo, verbose_name='发表文章用户', on_delete=models.CASCADE)
	lable = models.ForeignKey(CommnuityLable, verbose_name='文章标签', on_delete=models.CASCADE)
	commnuit_content = models.TextField(verbose_name='文章内容')
	create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
	update_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)
	click_num = models.IntegerField(verbose_name='点赞数', default=None)
	commnuit_img = models.ImageField(blank=True, verbose_name='文章图片')
	comment_num = models.IntegerField(verbose_name='文章评论数', default=None)

	class Meta:
		db_table = 'commnuity'
	def __str__(self):
		return 'id:%s commnuity_user:%s lable:%s commnuit_content:%s click_num:%s commnuit_img:%s' % (
			self.id, self.commnuity_user, self.lable, self.commnuit_content, self.click_num, self.commnuit_img)



	