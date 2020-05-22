# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room
import random

class ChatConsumer(AsyncWebsocketConsumer):
	@database_sync_to_async
	def join_room(self,room_name):
		r = Room.objects.get(title=room_name)
		r.occupants +=1
		r.save()
	@database_sync_to_async
	def leave_room(self, room_name):
		r = Room.objects.get(title=room_name)
		r.occupants -=1
		if r.occupants==0:
			r.delete()
		else:
			r.save()
	@database_sync_to_async
	def get_occupants(self, room_name):
		r = Room.objects.get(title=room_name)
		return r.occupants

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		# self.scope["session"]["seed"] = random.randint(1, 1000)
		# await print(self.channel_layer.group_channels(room_group_name))
		# Join room group
		await self.join_room(self.room_name)
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		occupants = await self.get_occupants(self.room_name)
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat.occupants',
				"count": occupants,
			},
		)

		await self.accept()


	async def disconnect(self, close_code):
		# Leave room group
		await self.leave_room(self.room_name)
		occupants = await self.get_occupants(self.room_name)
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat.occupants',
				"count": occupants,
			},
		)
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat.message',
				'message': message
			}
		)

	# Receive message from room group
	async def chat_message(self, event):
		message = event['message']

		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'msg_type': "message",
			'message': message
		}))

	async def chat_occupants(self, event):
		count = event['count']

		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'msg_type': "roomCount",
			'count': count
		}))

