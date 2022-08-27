import re
from typing import Union
from urllib.parse import ParseResult, urlparse

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf import settings
from django.urls import re_path
from strawberry.channels.handlers.http_handler import GraphQLHTTPConsumer
from strawberry.channels.handlers.ws_handler import GraphQLWSConsumer
from strawberry.schema import BaseSchema


class CorsGraphQLHTTPConsumer(GraphQLHTTPConsumer):
    _cors_headers: Union[dict, None]

    def __init__(self, **kwargs):
        self.allow_all_origins = getattr(settings, "CORS_ALLOW_ALL_ORIGINS", False)
        self.allowed_origins = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
        self._cors_headers = None
        super().__init__(**kwargs)

    async def send_headers(self, *, status=200, headers=None):
        """Add cors headers if applicable"""
        if headers is None:
            headers = []
        elif isinstance(headers, dict):
            headers = list(headers.items())

        if self._cors_headers:
            headers += [(k.encode(), v.encode()) for k, v in self._cors_headers.items()]

        await self.send({"type": "http.response.start", "status": status, "headers": headers})

    def regex_domain_match(self, origin: str) -> bool:
        return any(re.match(domain_pattern, origin) for domain_pattern in self.allowed_origins)

    def _url_in_allowlist(self, url: ParseResult) -> bool:
        origins = [urlparse(o) for o in self.allowed_origins]
        return any(origin.scheme == url.scheme and origin.netloc == url.netloc for origin in origins)

    def origin_found_in_allow_lists(self, origin: str, url: ParseResult) -> bool:
        return (
            (origin == "null" and origin in self.allowed_origins)
            or self._url_in_allowlist(url)
            or self.regex_domain_match(origin)
        )

    def set_cors_headers(self):
        origin = self.headers.get("origin")
        if not origin:
            return

        try:
            url = urlparse(origin)
        except ValueError:
            return

        if not self.origin_found_in_allow_lists(origin, url):
            return

        self._cors_headers = {
            "Access-Control-Allow-Origin": "*" if self.allow_all_origins else origin,
            "Access-Control-Allow-Headers": "*",
        }

    async def handle(self, body: bytes):
        self.set_cors_headers()
        if self.scope["method"] == "OPTIONS" and self.headers["access-control-request-method"]:
            await self.send_response(200, b"")
        await super().handle(body)


class GraphQLProtocolTypeRouter(ProtocolTypeRouter):
    """Similar to strawberry.channels.GraphQLProtocolTypeRouter"""

    def __init__(
        self,
        schema: BaseSchema,
        django_application=None,
        url_pattern="^graphql",
    ):
        http_urls = [re_path(url_pattern, CorsGraphQLHTTPConsumer.as_asgi(schema=schema))]
        if django_application is not None:
            http_urls.append(re_path("^", django_application))

        super().__init__(
            {
                "http": URLRouter(http_urls),
                "websocket": AllowedHostsOriginValidator(
                    URLRouter([re_path(url_pattern, GraphQLWSConsumer.as_asgi(schema=schema))])
                ),
            }
        )
