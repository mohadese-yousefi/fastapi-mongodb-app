from datetime import datetime

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from server.app.auth.schemas import TokenPayload
from server.core.settings import settings
from server.core.utils import CustomException


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl='user_token',
    scheme_name='JWT',
)

def get_current_user(token: str = Depends(reuseable_oauth)) ->  TokenPayload:
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expired',
            )
    except(
        jwt.exceptions.PyJWTError,
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.InvalidTokenError,
    ):
        raise CustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
        )
    
    return TokenPayload
 