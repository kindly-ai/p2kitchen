"""
ASGI config which exposes the ASGI callable as a module-level variable named ``application``.
Ref: https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from .router import GraphQLProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffeesite.settings")
django_asgi_app = get_asgi_application()

# Import your Strawberry schema after creating the django ASGI application
# This ensures django.setup() has been called before any ORM models are imported
# for the schema.
from p2coffee.schema import schema


application = GraphQLProtocolTypeRouter(schema, django_application=django_asgi_app)
