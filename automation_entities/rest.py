from typing import Any

import requests

from .context import Context
from .entities import Entity


class RestEntity(Entity):
    """
    entity for interacting with a REST API

    .. attribute:: base_url

        ``str`` representing the base URL of the REST API endpoint
    """

    def __init__(self, context: Context, base_url: str) -> None:
        self.context = context
        self.base_url = base_url
        super().__init__(context, self.base_url)

    def build_url(self, path: str) -> str:
        """
        build URL by appending the given *path* to the end of the
        :attr:`base_url`
        """
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")

    def new_request(self, method: str, path: str, **kwds: Any) -> requests.Request:
        """
        create and return a new :class:`requests.Request` instance with the
        given parameters
        """
        return requests.Request(method, self.build_url(path), **kwds)

    def send_request(self, request: requests.PreparedRequest) -> requests.Response:
        """
        send the given :class:`requests.Request` or
        :class:`requests.PreparedRequest`
        """
        with self.interaction():
            self.request(f"{request.method} {request.url}")

            session = requests.Session()
            resp = session.send(request)
            with self.result() as result:
                result.log(resp.content.decode())
                return resp

    def assert_send_request(
        self, request: requests.PreparedRequest
    ) -> requests.Response:
        """
        send the given :class:`requests.Request` or
        :class:`requests.PreparedRequest` and assert on its status code
        """
        resp = self.send_request(request)
        if resp.status_code < 200 or resp.status_code >= 400:
            raise AssertionError(f"[{resp.status_code}] {resp.text}")
        return resp
