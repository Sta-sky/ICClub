from haystack import indexes
from .models import Activity


class ActivityIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    subject = indexes.CharField(model_attr='subject')
    tag = indexes.CharField(model_attr='tag')
    content = indexes.CharField(model_attr='content')
    click_nums = indexes.CharField(model_attr='click_nums')
    def get_model(self):
        """返回建立索引的模型类"""
        return Activity


    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""

        return self.get_model().objects.all()
