import base64
import json
import secrets

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from .models import Message, Conversation
from .serializers import MessageSerializer

from django.core.cache import cache

from backend.settings import logger

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        conversation = Conversation.objects.get(id=int(self.room_name))
        if self.scope['user'] != conversation.initiator and self.scope['user'] != conversation.receiver:
            self.close()

        # Increment the connection counter
        self.increment_connection_count()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Decrement the connection counter
        self.decrement_connection_count()

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        # Check if all users have disconnected
        if self.get_connection_count() == 0:
            self.all_users_disconnected()

    # Receive message from WebSocket
    def receive(self, text_data, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        # Send message to room group
        chat_type = {"type": "chat_message"}
        realSender = {"realSender": self.scope['user'].username}
        return_dict = {**chat_type, **text_data_json, **realSender}
        #Save message in db
        message, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )
        conversation = Conversation.objects.get(id=int(self.room_name))
        sender = self.scope['user']

        # Attachment
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]

            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message = Message.objects.create(
                sender=sender,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
                realSender=realSender["realSender"],
            )
        else:
            _message = Message.objects.create(
                sender=sender,
                text=message,
                conversation_id=conversation,
                realSender=realSender["realSender"],
            )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Receive message from room group
    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        
        data_text = { "text": event["message"] }
        data_sender = { "realSender": event["realSender"] }
        data = {**data_text, **data_sender}
        #serializer = MessageSerializer(instance=_message)
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                data
            )
        )
    # Helper methods for managing connection count
    def get_connection_count(self):
        return cache.get(self.room_group_name, 0)

    def increment_connection_count(self):
        count = self.get_connection_count()
        cache.set(self.room_group_name, count + 1)

    def decrement_connection_count(self):
        count = self.get_connection_count()
        if count > 0:
            cache.set(self.room_group_name, count - 1)

    def all_users_disconnected(self):
        # Implement the logic for when all users have disconnected
        logger.warning(f"Room name: {self.room_name}")
        conversation = Conversation.objects.get(id=self.room_name)
        conversation.delete()
