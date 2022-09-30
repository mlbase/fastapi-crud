from typing import Tuple, List, Dict
from starlette import status
from jose import jwt

from config.setting import settings
from config import security
from schema.token import TokenPayload
from fastapi import HTTPException
from pydantic import ValidationError
import logging
logger = logging.getLogger()


#TODO middleware 분리하기 조사
#TODO starlette middleware로 authentication middleware 설계

async def token_decoder(token: str) -> Dict:
    print('start', token)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if not token_data.is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자가 아닙니다")
        print(token_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    except Exception as ex:
        if isinstance(ex, HTTPException):
            raise HTTPException
        logger.exception("uncaught error")
    return token_data

