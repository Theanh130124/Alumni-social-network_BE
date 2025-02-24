import json
from channels.generic.websocket import AsyncWebsocketConsumer

#Xử lý chat tg thực
from .security.security_mes import *

class ChatConsumer(AsyncWebsocketConsumer):
    #Kết nối
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await  self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await  self.accept()
    #Ngắt ket noi
    async  def disconnect(self, close_code):
        await  self.channel_layer.group_discard(self.room_group_name,self.channel_name)
    #Nhận dữ liệu từ client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        print("--------------------DECODE---------------------")
        print(decode_aes(message['content']))
        print("--------------------ENDCODE--------------------")

        message['content'] = decode_aes(message['content'])


        await  self.channel_layer.group_send(self.room_group_name,{"type":"chat_message","message":message})
    #Gửi dữ liệu đến client
    async  def chat_message(self,event):
        message = event["message"]

        await  self.send(text_data=json.dumps({"message":message}))