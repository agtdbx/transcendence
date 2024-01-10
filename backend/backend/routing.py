from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from backend.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/', ChatConsumer.as_asgi()),
    ])
})

# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/some_path/$', consumers.YourConsumer.as_asgi()),
#     # Ajoutez d'autres chemins WebSocket au besoin
# ]
