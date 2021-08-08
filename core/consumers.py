from channels.generic.websocket import JsonWebsocketConsumer


class AudioConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.accept()

    def receive_json(self, content, **kwargs):
        name = content['name']
        ctx = {**content, 'greeting': f'Hello {name}!!'}
        self.send_json(ctx)
