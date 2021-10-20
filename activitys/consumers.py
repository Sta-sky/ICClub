import json
from concurrent.futures import ThreadPoolExecutor
from urllib import parse
from urllib.parse import quote

from channels.generic.websocket import AsyncWebsocketConsumer, StopConsumer

from activitys.views import get_result


class OnlineConsumer(AsyncWebsocketConsumer):
	
	async def connect(self):
		print('.....websocket....connect.....')
		self.group_name = self.scope['url_route']['args'][0]
		self.room_group_name = 'active_%s' % self.group_name
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		print(f'websocket 连接到{self.room_group_name}')
		await self.accept()
		pool = ThreadPoolExecutor()
		page = self.scope['url_route']['args'][0]
		label = self.scope['query_string'].decode()
		if label:
			lab = parse.unquote(label)
			label = lab.split('=')[1]
		res = pool.submit(get_result, page, label)
		pool.shutdown(wait=True)
		active_list = res.result()
		await self.send(text_data=json.dumps(active_list))


	
	async def disconnect(self, code):
		self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		await self.close(code)
		raise StopConsumer()
	
	async def receive(self, text_data=None, bytes_data=None):
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'info',
				'message': json.dumps({'message': text_data})
			}
		)
		print('发送成功')

	async def info(self, event):
		await self.send(event['message'])
		
	async def send_info(self, event):
		print('send_info 群发消息')
		info = event['message']
		await self.send(json.dumps(info))

