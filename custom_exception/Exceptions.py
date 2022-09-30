from typing import Dict


class ExceptionBase(Exception):
    status_code: int
    detail: str = None
    dev: str = None
    content: dict = {
        "detail": detail,
        "dev": dev
    }


    def __str__(self) -> str:
        return "{ status_code: " + str(self.status_code) + \
               ", detail: " + self.detail + \
               ", dev: " + self.dev + "}"

    def __repr__(self) -> Dict:
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "dev": self.dev
        }

    def set_content(self, dev, detail):
        self.content["dev"] = dev
        self.content["detail"] = detail




class InvalidateUserException(ExceptionBase):
    def __init__(self):
        self.status_code = 400
        self.detail = "이메일 또는 비밀번호가 정확하지 않습니다"
        self.dev = "login is not valid"
        self.set_content(detail=self.detail, dev=self.dev)


class SQLException(ExceptionBase):
    def __init__(self):
        self.status_code = 500
        self.detail = "고객센터에 문의하세요"
        self.dev = "sql syntax error"
        self.set_content(detail=self.detail, dev=self.dev)


class AuthorizationException(ExceptionBase):
    def __init__(self):
        self.status_code = 401
        self.detail = "권한이 없습니다"
        self.dev = "validate token is needed"
        self.set_content(detail=self.detail, dev=self.dev)