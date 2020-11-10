# *-* coding=utf8 *-*
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts='http://localhost:9200')
# for i in range(100):
# 	es.delete(index='djangotest', id='activ.activity.' + str(i+1))

data = es.search(index='django_search')
print(data)


# {
# 	'took': 52,
# 	'timed_out': False,
# 	'_shards': {
# 		'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0
# 	},
# 	'hits':
# 		{
# 			'total':
# 				{
# 					'value': 12,
# 					'relation': 'eq'
# 				},
# 			'max_score': 1.0,
# 			'hits':
# 				[
# 					{
# 						'_index': 'djangotest',
# 						'_type': 'modelresult',
# 						'_id': 'activ.activity.1',
# 						'_score': 1.0,
# 						'_source': {
# 							'id': 'activ.activity.1',
# 							'django_ct': 'activ.activity',
# 							'django_id': '1',
# 							'text': '1\n喜欢一个人 始于颜值 敬于才华 合于性格 久于善良 终于人品\n突然有种想去放牛的感觉，没有生活压力，没有江湖套路，没有爱恨情仇，只关心我的牛还在不在，以我的智商，只放一只，多了我也数不过来。它吃草，我睡觉。',
# 							'subject': '喜欢一个人 始于颜值 敬于才华 合于性格 久于善良 终于人品',
# 							'tag': 'id:1 nickname:音乐',
# 							'content': '突然有种想去放牛的感觉，没有生活压力，没有江湖套路，没有爱恨情仇，只关心我的牛还在不在，以我的智商，只放一只，多了我也数不过来。它吃草，我睡觉。'
# 						}
# 					},
# 					{
# 						'_index': 'djangotest',
# 						'_type': 'modelresult',
# 						'_id': 'activ.activity.2',
# 						'_score': 1.0,
# 						'_source': {
# 							'id': 'activ.activity.2',
# 							'django_ct': 'activ.activity',
# 							'django_id': '2',
# 							'text': '2\n日益努力，而后风生水起，众生皆苦，你也不能认输。\n在穷的只剩下梦想的时候，你一定要比别人更加努力。我们用人生最好的年华作抵押，去担保一个说出来都会被嘲笑的梦想。累么？累就对了，舒服是留给死人的！',
# 							'subject': '日益努力，而后风生水起，众生皆苦，你也不能认输。',
# 							'tag': 'id:1 nickname:音乐',
# 							'content': '在穷的只剩下梦想的时候，你一定要比别人更加努力。我们用人生最好的年华作抵押，去担保一个说出来都会被嘲笑的梦想。累么？累就对了，舒服是留给死人的！'
# 						}
# 					},
# 					{
# 						'_index': 'djangotest',
# 						'_type': 'modelresult',
# 						'_id': 'activ.activity.3',
# 						'_score': 1.0,
# 						'_source': {
# 							'id': 'activ.activity.3',
# 							'django_ct': 'activ.activity',
# 							'django_id': '3', 'text': '3\n想一千次，不如去做一次，华丽的跌倒，胜过无谓的徘徊，输不起的人往往也赢不了，如果自己不努力，那么这一辈子只可能在原地踏步\n别让你的努力，毁于低效率的勤奋。低效率的勤奋往往流于形式，忽略了真实的努力，不过是为了让自己心安罢了。勤奋不是嘴上说说而已，而是内心真正的渴望和热忱。', 'subject': '想一千次，不如去做一次，华丽的跌倒，胜过无谓的徘徊，输不起的人往往也赢不了，如果自己不努力，那么这一辈子只可能在原地踏步', 'tag': 'id:1 nickname:音乐', 'content': '别让你的努力，毁于低效率的勤奋。低效率的勤奋往往流于形式，忽略了真实的努力，不过是为了让自己心安罢了。勤奋不是嘴上说说而已，而是内心真正的渴望和热忱。'}}, {'_index': 'djangotest', '_type': 'modelresult', '_id': 'activ.activity.4', '_score': 1.0, '_source': {'id': 'activ.activity.4', 'django_ct': 'activ.activity', 'django_id': '4', 'text': '4\n每个人身上都有惰性和消极情绪，成功的人都是懂\n年轻，那么短暂，那么迷茫。如果你不能给自己一张耀眼的文凭、一段荡气回肠的爱情，那么，你还可以给自己一个九成九会遭到嘲笑的梦想。因为，总有一天，它会让你闪闪发光。', 'subject': '每个人身上都有惰性和消极情绪，成功的人都是懂', 'tag': 'id:2 nickname:游泳', 'content': '年轻，那么短暂，那么迷茫。如果你不能给自己一张耀眼的文凭、一段荡气回肠的爱情，那么，你还可以给自己一个九成九会遭到嘲笑的梦想。因为，总有一天，它会让你闪闪发光。'}}, {'_index': 'djangotest', '_type': 'modelresult', '_id': 'activ.activity.5', '_score': 1.0, '_source': {'id': 'activ.activity.5', 'django_ct': 'activ.activity', 'django_id': '5', 'text': '5\n每一个成功者都是一位苦行僧，只有他们自己才知\n对于攀登者来说，失掉往昔的足迹并不可惜，迷失了继续前进的方向却很危险。平凡的脚步也可以走完伟大的行程。当你觉的累的时候就看看那些还在努力的人。', 'subject': '每一个成功者都是一位苦行僧，只有他们自己才知', 'tag': 'id:3 nickname:跑步', 'content': '对于攀登者来说，失掉往昔的足迹并不可惜，迷失了继续前进的方向却很危险。平凡的脚步也可以走完伟大的行程。当你觉的累的时候就看看那些还在努力的人。'}}, {'_index': 'djangotest', '_type': 'modelresult', '_id': 'activ.activity.6', '_score': 1.0, '_source': {'id': 'activ.activity.6', 'django_ct': 'activ.activity', 'django_id': '6', 'text': '6\n做人如水，你高，我便退去\n做人如水，你高，\n\n我便退去，决不淹没你的优点;\n\n做人如水，你低，\n\n我便涌来，决不暴露你的缺陷;\n\n做人如水，你动，\n\n我便随行，决不撇下你的孤单;', 'subject': '做人如水，你高，我便退去', 'tag': 'id:6 nickname:动漫', 'content': '做人如水，你高，\n\n我便退去，决不淹没你的优点;\n\n做人如水，你低，\n\n我便涌来，决不暴露你的缺陷;\n\n做人如水，你动，\n\n我便随行，决不撇下你的孤单;'}}, {'_index': 'djangotest', '_type': 'modelresult', '_id': 'activ.activity.7', '_score': 1.0, '_source': {'id': 'activ.activity.7', 'django_ct': 'activ.activity', 'django_id': '7', 'text': '7\n敏感却不执着，坚定而又变通；稳重但又热烈，成\n他们的逞强，其实是需要外界的认可，究其本质，还是因为内心不够强大，所以才活在别人眼里。\n\n他们特别在意别人的看法，总是活在他人的眼目口舌之中，而且特别喜欢解释，生怕别人看低了自己，这是内心自卑的表现。', 'subject': '敏感却不执着，坚定而又变通；稳重但又热烈，成', 'tag': 'id:8 nickname:骑行', 'content': '他们的逞强，其实是需要外界的认可，究其本质，还是因为内心不够强大，所以才活在别人眼里。\n\n他们特别在意别人的看法，总是活在他人的眼目口舌之中，而且特别喜欢解释，生怕别人看低了自己，这是内心自卑的表现。'}}, {'_index': 'djangotest', '_type': 'modelresult', '_id': 'activ.activity.8', '_score': 1.0, '_source': {'id': 'activ.activity.8', 'django_ct': 'activ.activity', 'django_id': '8', 'text': '8\n高度自律但又能随时自黑\n因为人的自律往往缘于自强，人的自黑往往源于自信。\n\n我们可以打倒一个站着的人，但是却很难打倒一个本来就躺在地上的人', 'subject': '高度自律但又能随时自黑', 'tag': 'id:8 nickname:骑行', 'content': '因为人的自律往往缘于自强，人的自黑往往源于自信。\n\n我们可以打倒一个站着的人，但是却很难打倒一个本来就躺在地上的人'}}, {'_index': 'djangotest', '_type': 'modelresult', '_id': 'activ.activity.9', '_score': 1.0, '_source': {'id': 'activ.activity.9', 'django_ct': 'activ.activity', 'django_id': '9', 'text': '9\n阳光下像个孩子，风雨里像个大人；得到了不狂喜\n阳光下像个孩子，风雨里像个大人；得到了不狂喜，失去了不伤悲。\n\n把失败当寻常，把成功当恩赐', 'subject': '阳光下像个孩子，风雨里像个大人；得到了不狂喜', 'tag': 'id:8 nickname:骑行', 'content': '阳光下像个孩子，风雨里像个大人；得到了不狂喜，失去了不伤悲。\n\n把失败当寻常，把成功当恩赐'}}, {'_index': 'djangotest', '_type': 'modelresult', '_id': 'activ.activity.10', '_score': 1.0, '_source': {'id': 'activ.activity.10', 'django_ct': 'activ.activity', 'django_id': '10', 'text': '10\n年轻，那么短暂，那么迷茫。如果你不能给自己一\n一段荡气回肠的爱情，那么，你还可以给自己一个九成九会遭到嘲笑的梦想。因为，总有一天，它会让你闪闪发光。', 'subject': '年轻，那么短暂，那么迷茫。如果你不能给自己一', 'tag': 'id:3 nickname:跑步', 'content': '一段荡气回肠的爱情，那么，你还可以给自己一个九成九会遭到嘲笑的梦想。因为，总有一天，它会让你闪闪发光。'}}]}}