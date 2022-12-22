import typing


from starlette.datastructures import URL, Headers
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

ENFORCE_DOMAIN_WILDCARD = "Domain wildcard patterns must be like '*.example.com'."

# starlette에 정의되어 있는 미들웨어 (except_path를 정의하기 위해 재정의)
# 도메인을 지정하여 지정한 도메인으로 요청했을 때만 그 요청이 유효하다고 인정하는 미들웨어
class TrustedHostMiddleware:
  def __init__(
    self,
    app: ASGIApp,
    allowed_hosts: typing.Sequence[str] = None,
    except_path: typing.Sequence[str] = None, 
    # 로드밸런서를 사용할 때, 로드밸런서에서 내부 ip로 health check를 수행하는데
    # health check를 할 때 정해놓은 호스트를 사용하지 않고 ip주소를 사용함.
    # 따라서 except_path가 없으면 health check를 실패함. -> 로드 밸런서는 서버가 죽었다고 인지
    www_redirect: bool = True,
  ) -> None:
    if allowed_hosts is None:
      allowed_hosts = ["*"]
    if except_path is None:
      except_path = []
    for pattern in allowed_hosts:
      assert "*" not in pattern[1:], ENFORCE_DOMAIN_WILDCARD
      if pattern.startswith("*") and pattern != "*":
        assert pattern.startswith("*."), ENFORCE_DOMAIN_WILDCARD
    self.app = app
    self.allowed_hosts = list(allowed_hosts)
    self.allow_any = "*" in allowed_hosts
    self.www_redirect = www_redirect
    self.except_path = list(except_path)

  async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
    if self.allow_any or scope["type"] not in ("http", "websocket",):  # pragma: no cover
      await self.app(scope, receive, send)
      return
      
    headers = Headers(scope=scope)
    host = headers.get("host", "").split(":")[0]
    is_valid_host = False
    found_www_redirect = False
    for pattern in self.allowed_hosts:
      if (
        host == pattern
        or (pattern.startswith("*") and host.endswith(pattern[1:]))
        or URL(scope=scope).path in self.except_path
      ):
        is_valid_host = True
        break
      elif "www." + host == pattern:
        found_www_redirect = True
    if is_valid_host:
      await self.app(scope, receive, send)
    else:
      if found_www_redirect and self.www_redirect:
        url = URL(scope=scope)
        redirect_url = url.replace(netloc="www." + url.netloc)
        response = RedirectResponse(url=str(redirect_url))  # type: Response
      else:
        response = PlainTextResponse("Invalid host header", status_code=400)
      await response(scope, receive, send)