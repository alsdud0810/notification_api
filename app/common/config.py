from dataclasses import dataclass
from os import path, environ
from typing import List

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
  """
  기본 Configuration
  """
  BASE_DIR: str = base_dir
  
  DB_POOL_RECYCLE: int = 900
  DB_ECHO: bool = True

@dataclass
class LocalConfig(Config):
  PROJ_RELOAD: bool = True
  DB_URL: str = "postgresql://postgres:123@localhost:5432/notification_api"
  TRUSTED_HOSTS=["*"]
  ALLOW_SITE = ["*"]


@dataclass
class ProdConfig(Config):
  PROJ_RELOAD: bool = True
  TRUSTED_HOSTS=["*"]
  ALLOW_SITE = ["*"]


def conf():
  """
  환경 불러오기
  :return:
  """
  config = dict(prod=ProdConfig, local=LocalConfig())
  return config[environ.get("API_ENV", "local")]

