from django.db import models

class CommnuityLable(models.Model):
	lable_name = models.CharField(max_length=20, verbose_name='论坛标签名')
	img_url = models.ImageField(blank=True, verbose_name='标签默认图片')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Mete:
		db_table = 'commnuity_lable'

	def __str__(self):
		return 'id:%s lable_name:%s img_url:%s' % (self.id, self.lable_name, self.img_url)

class Article(models.Model):
	commnuity_user = models.IntegerField(verbose_name='发表文章用户')
	lable = models.CharField(max_length=100, verbose_name='文章标签')
	commnuit_content = models.TextField(verbose_name='文章内容')
	create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
	update_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)
	click_num = models.IntegerField(verbose_name='点赞数', default=0)
	commnuit_img = models.ImageField(blank=True, verbose_name='文章图片')
	comment_num = models.IntegerField(verbose_name='文章评论数', default=0)

	class Meta:
		db_table = 'Article'
	def __str__(self):
		return 'id:%s commnuity_user:%s lable:%s commnuit_content:%s click_num:%s commnuit_img:%s' % (
			self.id, self.commnuity_user, self.lable, self.commnuit_content, self.click_num, self.commnuit_img)

class comment(models.Model):
	comment_user = models.IntegerField(verbose_name='评论用户')
	commented_user = models.IntegerField(verbose_name='被评论用户')
	content = models.CharField(max_length=500, verbose_name='评论内容')
	article = models.ForeignKey(Article, verbose_name='所属文章', on_delete=models.CASCADE)
	comment_subid = models.CharField(max_length=100, verbose_name='子级评论')
	comment_pid = models.CharField(max_length=100, verbose_name='父级评论')
	is_primery = models.IntegerField(verbose_name='是否是一级评论', default=1)


	