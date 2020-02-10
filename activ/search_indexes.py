

from haystack import indexes
from .models import Activity


class ActivityIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    # subject = models.CharField(max_length=100, verbose_name='活动主题')
    subject = indexes.CharField(model_attr='subject')
    tag = indexes.CharField(model_attr='tag')
    def get_model(self):
        """返回建立索引的模型类"""
        return Activity


    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""

        return self.get_model().objects.filter(is_visiable=True)

        # return self.get_model().objects.all()


# WARNING: This will irreparably remove EVERYTHING from your search index in connection 'default'.
# Your choices after this are to restore from backups or rebuild via the `rebuild_index` command.
# Are you sure you wish to continue? [y/N] y
# Removing all documents from your index because you said so.
# All documents removed.
# Indexing 26 活动创建表
# GET /djangotest/_mapping [status:404 request:0.003s]


"""
{
  "djangotest": {
    "mappings": {
      "modelresult": {
        "properties": {
          "django_ct": {
            "type": "string",
            "index": "not_analyzed",
            "include_in_all": false
          },
          "django_id": {
            "type": "string",
            "index": "not_analyzed",
            "include_in_all": false
          },
          "id": {
            "type": "string"
          },
          "subject": {
            "type": "string",
            "analyzer": "snowball"
          },
          "text": {
            "type": "string",
            "analyzer": "snowball"
          }
        }
      }
    }
  }
}"""

