from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from database.conn import db
from common.config import conf
# from middlewares.token_validator import access_control
from middlewares.token_validator import AccessControl
from common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX
from middlewares.trusted_hosts import TrustedHostMiddleware
from routes import index, auth

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

def create_app():

  c = conf()
  app = FastAPI()
  conf_dict = asdict(c)
  db.init_app(app, **conf_dict)

  # 데이터 베이스 이니셜라이즈

  # 레디스 이니셜라이즈

  # 미들웨어 정의
  # app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
  app.add_middleware(AccessControl, except_path_list=EXCEPT_PATH_LIST, except_path_regex=EXCEPT_PATH_REGEX)
  app.add_middleware(
    CORSMiddleware, # abc.com에서 abc.com 호스트로만 접속을 할 수 있게하는
    allow_origins=conf().ALLOW_SITE,
    allow_credentials=True,
    # 일단은(개발할 때는) 누구든 접속할 수 있도록 (프론트와 백 도메인 주소가 달라도 접속 가능)
    allow_methods=["*"],
    allow_headers=["*"],
  )
  app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])
  # 주의 - 미들웨어 순서 (오류가 없으면 밑에서 순차적으로 수행 -> 최종적으로 user한테 응답 전달)


  # 라우터 정의
  app.include_router(index.router)
  # app.include_router(auth.router, tags=["Authentication"])
  app.include_router(auth.router, tags=["Authentication"], prefix="/api")

  return app

app = create_app()

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=conf().PROJ_RELOAD)