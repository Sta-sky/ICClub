# -*- coding: utf-8 -*-
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^active/new/(\d+)$",consumers.OnlineConsumer.as_asgi())
]

