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


# WARNING: This will irreparably remove EVERYTHING from your search index in connection 'default'.
# Your choices after this are to restore from backups or rebuild via the `rebuild_index` command.
# Are you sure you wish to continue? [y/N] y
# Removing all documents from your index because you said so.
# All documents removed.
# Indexing 26 活动创建表
# GET /djangotest/_mapping [status:404 request:0.003s]


"""
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ngram_analyzer": {
          "tokenizer": "ngram_tokenizer"
        }
      },
      "tokenizer": {
        "ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 1,
          "max_gram": 30,
          "token_chars": [
            "letter",
            "digit"
          ]
        }
      }
    }
  },
  "mappings": {
        "_default_": {
            "properties": {
                "Name": {
                    "type": "string",
                    "analyzer": "ngram_analyzer"
                }
            }
        }
    }
}
"""