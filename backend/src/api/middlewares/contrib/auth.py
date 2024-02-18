import typing
import inspect
import functools
import asyncio
from urllib.parse import urlencode
from starlette.exceptions import HTTPException
from starlette.requests import Request, HTTPConnection
from starlette.responses import RedirectResponse, Response
from starlette.websockets import WebSocket


def has_required_scope(conn: HTTPConnection, scopes: typing.Sequence[str], scopes_disjunctive: bool = True) -> bool:
    if scopes_disjunctive:
        if len(scopes) == 0:
            # No permission is required
            return True
        for scope in scopes:
            if scope in conn.auth.scopes:
                return True
        return False
    
    ## scopes should be checked conjunctively
    for scope in scopes:
        if scope not in conn.auth.scopes:
            return False
    return True

def requires(
    scopes: typing.Union[str, typing.Sequence[str]],
    status_code: int = 403,
    # type_: str = 'request',
    redirect: typing.Optional[str] = None,
    scopes_disjunctive: bool = True,
) -> typing.Callable:
    scopes_list = [scopes] if isinstance(scopes, str) else list(scopes)

    def decorator(func: typing.Callable) -> typing.Callable:
        sig = inspect.signature(func)
        for idx, parameter in enumerate(sig.parameters.values()):
            if parameter.name == "request" or parameter.name == "websocket":
                type_ = parameter.name
                break
        else:
            raise Exception(
                f'No "request" or "websocket" argument on function "{func}"'
            )

        if type_ == "websocket":
            # Handle websocket functions. (Always async)
            @functools.wraps(func)
            async def websocket_wrapper(
                *args: typing.Any, **kwargs: typing.Any
            ) -> None:
                websocket = kwargs.get(
                    "websocket", args[idx] if idx < len(args) else None
                )
                assert isinstance(websocket, WebSocket)

                if not has_required_scope(websocket, scopes_list):
                    await websocket.close()
                else:
                    await func(*args, **kwargs)

            return websocket_wrapper

        elif asyncio.iscoroutinefunction(func):
            # Handle async request/response functions.
            @functools.wraps(func)
            async def async_wrapper(
                *args: typing.Any, **kwargs: typing.Any
            ) -> Response:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                assert isinstance(request, Request)

                if not has_required_scope(request, scopes_list, scopes_disjunctive=scopes_disjunctive):
                    if redirect is not None:
                        orig_request_qparam = urlencode({"next": str(request.url)})
                        next_url = "{redirect_path}?{orig_request}".format(
                            redirect_path=request.url_for(redirect),
                            orig_request=orig_request_qparam,
                        )
                        return RedirectResponse(url=next_url, status_code=303)
                    raise HTTPException(status_code=status_code)
                return await func(*args, **kwargs)

            return async_wrapper

        else:
            # Handle sync request/response functions.
            @functools.wraps(func)
            def sync_wrapper(*args: typing.Any, **kwargs: typing.Any) -> Response:
                request = kwargs.get("request", args[idx] if idx < len(args) else None)
                assert isinstance(request, Request)

                if not has_required_scope(request, scopes_list, scopes_disjunctive=scopes_disjunctive):
                    if redirect is not None:
                        orig_request_qparam = urlencode({"next": str(request.url)})
                        next_url = "{redirect_path}?{orig_request}".format(
                            redirect_path=request.url_for(redirect),
                            orig_request=orig_request_qparam,
                        )
                        return RedirectResponse(url=next_url, status_code=303)
                    raise HTTPException(status_code=status_code)
                return func(*args, **kwargs)

            return sync_wrapper

    return decorator