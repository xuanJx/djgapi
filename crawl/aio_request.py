from __future__ import absolute_import, division, with_statement

import asyncio
import aiohttp
import sys
import traceback
import contextlib
import logging

from functools import partial
from multidict import CIMultiDict
from typing import (
    Mapping,
    Union,
    Optional,
    Any,
    Awaitable,
    Dict,
    Type,
    Callable,
    Coroutine,
    Generator,
    AsyncGenerator,
    TypeVar,
    AsyncContextManager,
)
from aiohttp.typedefs import (
    StrOrURL, LooseHeaders
)
from aiohttp.abc import (
    AbstractCookieJar
)
from types import TracebackType

logger = logging.getLogger('Aio_request')

__all__ = [
    'get',
    'post',
    'get_json',
    'get_text',
    'get_read',
    'AioRequestClient',
]

# TODO: 完成连接池同时连接的数量控制

ENABLE_PROXY = False
PROXY_URL = 'http://127.0.0.1:1080'
PROXY_AUTH = False
PROXY_USER = ''
PROXY_PASSWORD = ''
GLOBAL_MAX_RETRY = 5

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"  # noqa

SUPPORTED_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "HEAD",
]


_RetType = TypeVar("_RetType")


if ENABLE_PROXY and sys.platform == 'win32':
    # windows下需要使用WindowsSelectorEventLoopPolicy才能使用http代理访问https
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_running_loop(
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> asyncio.AbstractEventLoop:
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop

def get_session(**kwargs: Any) -> aiohttp.ClientSession:
    cookie_jar = kwargs.get("cookie_jar", None)
    if cookie_jar is None:
        # aiohttp严格模式按照 RFC2109
        # 明确禁止接收url和ip地址产生的cookie，
        # 只能接收dns解析IP产生的cookie，设置unsafe=True取消
        cookie_jar = aiohttp.CookieJar(unsafe=True)
        kwargs.update({"cookie_jar": cookie_jar})
    return aiohttp.ClientSession(**kwargs)


def get_text(response: aiohttp.ClientResponse) -> Awaitable[str]:
    return response.text(encoding='utf-8')


def get_json(response: aiohttp.ClientResponse) -> Awaitable[Any]:
    return response.json()


def get_read(response: aiohttp.ClientResponse) -> Awaitable[bytes]:
    return response.read()


class ExceededMaxRetriesRequestError(Exception):
    pass


class FetchContextManager:

    def __init__(
        self,
        coro: Coroutine[asyncio.Future[Any], None, _RetType]
    ) -> None:
        self._coro = coro

    def __await__(self) -> Generator[Any, None, _RetType]:
        ret = self._coro.__await__()
        return ret

    def __iter__(self) -> Generator[Any, None, _RetType]:
        return self.__await__()


@contextlib.asynccontextmanager
async def retryRequestContextManager(
    *,
    fetch: Callable[..., Any],
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **fetch_kwargs: Any
) -> AsyncGenerator[Any, None]:

    count = 0

    if not retry_request:
        # disabled retry request
        _max_retry = 1
    else:
        _max_retry = GLOBAL_MAX_RETRY
        if isinstance(max_retry, int) and max_retry >= 1:
            _max_retry = max_retry

    exc = None
    done = False

    while count < _max_retry:
        try:
            result = await FetchContextManager(fetch(**fetch_kwargs)) # type: aiohttp.ClientResponse
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            logger.warning(f'An exception occurred in a request: {e}')
            if raise_exc:
                exc = e
        else:
            done = True
            yield result
        finally:
            count += 1

    if not done:
        if isinstance(exc, Exception):
            raise exc
        msg = "The client request is exceeded the max retries."
        logger.error(msg)
        raise ExceededMaxRetriesRequestError(msg)


def _fetch_get(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    url_params: Optional[Mapping[str, str]] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:
    return _fetch(
        session,
        url,
        "get",
        url_params,
        headers=headers,
        is_json=is_json,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


def _fetch_post(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    data: Optional[Any] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:
    return _fetch(
        session,
        url,
        "post",
        data,
        headers=headers,
        is_json=is_json,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


def _fetch_put(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    data: Optional[Any] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:
    return _fetch(
        session,
        url,
        "put",
        data,
        headers=headers,
        is_json=is_json,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


def _fetch_patch(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    data: Optional[Any] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:
    return _fetch(
        session,
        url,
        "patch",
        data,
        headers=headers,
        is_json=is_json,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


def _fetch_delete(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    data: Optional[Any] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:
    return _fetch(
        session,
        url,
        "delete",
        data,
        headers=headers,
        is_json=is_json,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


def _fetch_options(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    data: Optional[Any] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[int] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:
    return _fetch(
        session,
        url,
        "options",
        data,
        headers=headers,
        is_json=is_json,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


def _fetch_head(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    data: Optional[Any] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,
    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:
    return _fetch(
        session,
        url,
        "head",
        data,
        headers=headers,
        is_json=is_json,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


def _fetch(
    session: aiohttp.ClientSession,
    url: StrOrURL,
    method: str,
    data: Optional[Any] = None,
    *,
    headers: Optional[LooseHeaders] = None,
    is_json: bool = False,
    timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: Optional[bool] = None,

    **kwargs: Any
) -> AsyncContextManager[aiohttp.ClientResponse]:

    method_upper = method.upper()
    method_lower = method.lower()

    if method_upper not in SUPPORTED_METHODS:
        raise ValueError(f"Unsupported method <{method_upper}>")

    params: Dict[str, Any] = {"url": url}

    if data is not None:
        if method_upper == "GET":
            params.update({"params": data})
        elif is_json and isinstance(data, dict):
            params.update({"json": data})
        else:
            params.update({"data": data})

    if isinstance(headers, dict):
        params.update({"headers": headers})

    if (isinstance(timeout, int)
            or isinstance(timeout, aiohttp.ClientTimeout)):
        params.update({"timeout": timeout})

    if kwargs:
        params.update(kwargs)

    if ENABLE_PROXY:
        params.update({"proxy": PROXY_URL})
        if PROXY_AUTH:
            proxy_auth = aiohttp.BasicAuth(PROXY_USER, PROXY_PASSWORD)
            params.update({"proxy_auth": proxy_auth})

    fetch = getattr(session, method_lower)
    context_manager = partial(
        retryRequestContextManager,
        fetch=fetch,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **params
    )
    return context_manager()


async def _request(
    fetch: Callable[..., Any],
    url: StrOrURL,
    data: Optional[Any] = None,
    *,
    resp_callback: Callable[[aiohttp.ClientResponse], Any] = get_read,
    headers: Optional[Mapping[str, str]] = None,
    is_json: bool = False,
    cookies: Optional[Mapping[str, str]] = None,
    timeout: Optional[int] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: bool = True,
    **kwargs: Any
) -> Any:
    headers_dict = {
        "User-Agent": USER_AGENT
    }

    if isinstance(headers, dict):
        headers_dict.update(headers)

    async with get_session(
            headers=headers_dict,
            cookies=cookies or {},
            **kwargs
    ) as session:
        async with fetch(
            session,
            url,
            data,
            is_json=is_json,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
        ) as resp:
            return await resp_callback(resp)


async def get(
    url: StrOrURL,
    headers: Optional[Mapping[str, str]] = None,
    data: Optional[Any] = None,
    *,
    is_json: bool = False,
    resp_callback: Callable[[aiohttp.ClientResponse], Any] = get_read,
    timeout: Optional[int] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: bool = True,
    **kwargs: Any
) -> Any:
    if is_json:
        if not isinstance(headers, dict):
            headers = dict()
        headers.update({"Content-Type": "application/json"})
    return await _request(
        _fetch_get,
        url,
        data,
        headers=headers,
        resp_callback=resp_callback,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


async def post(
    url: StrOrURL,
    headers: Optional[Mapping[str, str]] = None,
    data: Optional[Any] = None,
    *,
    is_json: bool = False,
    resp_callback: Callable[[aiohttp.ClientResponse], Any] = get_read,
    timeout: Optional[int] = None,
    retry_request: Optional[bool] = None,
    max_retry: Optional[int] = None,
    raise_exc: bool = True,
    **kwargs: Any
) -> Any:
    if is_json:
        if not isinstance(headers, dict):
            headers = dict()
        headers.update({"Content-Type": "application/json"})
    return await _request(
        _fetch_post,
        url,
        data,
        headers=headers,
        is_json=is_json,
        resp_callback=resp_callback,
        timeout=timeout,
        retry_request=retry_request,
        max_retry=max_retry,
        raise_exc=raise_exc,
        **kwargs
    )


class AioRequestClient(object):

    _source_traceback = None

    def __init__(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
        is_json: bool = False,
        cookie_jar: Optional[AbstractCookieJar] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        timeout: Optional[Union[aiohttp.ClientTimeout, int]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: bool = True,
        **client_session_kwargs: Any
    ) -> None:
        self._session = None   # type: Optional[aiohttp.ClientSession]
        self._headers = headers if isinstance(headers, dict) else dict()
        self._is_json = is_json
        self._cookie_jar = cookie_jar
        self._closed = True
        self._loop = get_running_loop(loop)

        if timeout is not None:
            timeout = timeout if isinstance(timeout, aiohttp.ClientTimeout)\
                else aiohttp.ClientTimeout(total=timeout)
        self._timeout = timeout

        self._retry_request = retry_request
        self._max_retry = max_retry
        self._raise_exc = raise_exc

        if self._loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        self._client_session_kwargs = client_session_kwargs

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._closed:
            session = self._create_session()
            self._session = session
        return self._session  # type: ignore

    def get_headers(self) -> Dict[str, str]:
        headers = self._headers
        headers.update({
            "User-Agent": USER_AGENT
        })
        return headers

    def add_headers(self, headers: Optional[Mapping[str, str]] = None) -> None:
        if headers and isinstance(headers, dict):
            self._headers.update(headers)
            self._update_session_headers()

    def del_header(self, keyword: str) -> None:
        if keyword in self._headers.keys():
            self._headers.pop(keyword)
            self._update_session_headers()

    def _update_session_headers(self) -> None:
        if not self._closed and self.session:
            headers = self.get_headers()
            self.session._default_headers = CIMultiDict(headers)

    def add_cookies(self, cookies: Optional[Mapping[str, str]] = None) -> None:
        if ((cookies and isinstance(cookies, dict))
                and (not self._closed and self.session)):
            self.session._cookie_jar.update_cookies(cookies)

    def set_timeout(self, timeout: int = 500) -> None:
        if isinstance(timeout, int) and (not self._closed and self.session):
            self.session._timeout = aiohttp.ClientTimeout(total=timeout)

    def get_session(self, **kwargs: Any) -> aiohttp.ClientSession:
        if self._session:
            return self._session

        if self._closed:
            self._closed = False

        session = self._create_session(**kwargs)
        self._session = session

        return self.session

    def _create_session(self, **kwargs: Any) -> aiohttp.ClientSession:
        headers_dict = self.get_headers()
        kwargs.update({
            "headers": headers_dict,
            "cookie_jar": self._cookie_jar,
            "loop": self._loop
        })

        if self._timeout is not None:
            kwargs.update({"timeout": self._timeout})

        if self._client_session_kwargs:
            kwargs.update(self._client_session_kwargs)

        return get_session(**kwargs)

    def get(
        self,
        url: StrOrURL,
        url_params: Optional[Mapping[str, str]] = None,
        *,
        headers: Optional[LooseHeaders] = None,
        is_json: bool = False,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any,
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        return self._request(
            _fetch_get,
            url,
            url_params,
            headers=headers,
            timeout=timeout,
            is_json=is_json,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    def post(
        self,
        url: StrOrURL,
        data: Optional[Any] = None,
        *,
        headers: Optional[LooseHeaders] = None,
        is_json: bool = False,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        return self._request(
            _fetch_post,
            url,
            data,
            headers=headers,
            is_json=is_json,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    def put(
        self,
        url: StrOrURL,
        data: Optional[Any] = None,
        *,
        headers: Optional[LooseHeaders] = None,
        is_json: bool = False,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        return self._request(
            _fetch_put,
            url,
            data,
            headers=headers,
            is_json=is_json,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    def patch(
        self,
        url: StrOrURL,
        data: Optional[Any] = None,
        *,
        headers: Optional[LooseHeaders] = None,
        is_json: bool = False,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        return self._request(
            _fetch_patch,
            url,
            data,
            headers=headers,
            is_json=is_json,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    def delete(
        self,
        url: StrOrURL,
        data: Optional[Any] = None,
        *,
        headers: Optional[LooseHeaders] = None,
        is_json: bool = False,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        return self._request(
            _fetch_delete,
            url,
            data,
            headers=headers,
            is_json=is_json,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    def options(
        self,
        url: StrOrURL,
        *,
        headers: Optional[LooseHeaders] = None,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        return self._request(
            _fetch_options,
            url,
            headers=headers,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    def head(
        self,
        url: StrOrURL,
        *,
        headers: Optional[LooseHeaders] = None,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        return self._request(
            _fetch_head,
            url,
            headers=headers,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    def _request(
        self,
        fetch: Callable[..., AsyncContextManager],
        url: StrOrURL,
        data: Optional[Any] = None,
        *,
        headers: Optional[Mapping[str, str]] = None,
        is_json: bool = False,
        timeout: Optional[Union[int, aiohttp.ClientTimeout]] = None,
        retry_request: Optional[bool] = None,
        max_retry: Optional[int] = None,
        raise_exc: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncContextManager[aiohttp.ClientResponse]:
        is_json = is_json or self._is_json
        if is_json:
            if not isinstance(headers, dict):
                headers = dict()
            headers.update({"Content-Type": "application/json"})
        session = self.get_session()

        if retry_request is None:
            retry_request = self._retry_request

        if max_retry is None:
            max_retry = self._max_retry

        if raise_exc is None:
            raise_exc = self._raise_exc

        return fetch(
            session,
            url,
            data,
            headers=headers,
            is_json=is_json,
            timeout=timeout,
            retry_request=retry_request,
            max_retry=max_retry,
            raise_exc=raise_exc,
            **kwargs
        )

    async def close(self) -> None:
        if not self._closed:
            self._closed = True
            if self._session:
                await self._session.close()
            self._session = None

    def __del__(self) -> None:
        if not self._closed:
            context = {
                "AioRequestClient": self,
                "message": "Unclose AioRequestClient"}
            if self._source_traceback is not None:
                context["source_traceback"] = self._source_traceback
            self._loop.call_exception_handler(context)

    def __enter__(self) -> None:
        raise TypeError("Use async with instead")

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    async def __aenter__(self) -> "AioRequestClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()
