from channels.routing import URLRouter, ProtocolTypeRouter
import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

from activitys import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ICClub.settings')

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
	'http': django_asgi_app,
	'websocket': AuthMiddlewareStack(
		URLRouter(
			routing.websocket_urlpatterns
		)
	)
})
