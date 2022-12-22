JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)" # auth: 인증하는 endpoint는 토큰 검사 하면 안됨.