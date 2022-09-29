from typing import Callable, Any, Coroutine

from fastapi import Request, Response, HTTPException, APIRouter, FastAPI
from fastapi.routing import APIRoute
import logging


class RouteErrorHandler(APIRoute):

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as ex:
                body = await request.body()
                detail = {"errors": ex.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)
        return custom_route_handler()



