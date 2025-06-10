from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_db
from passlib.context import CryptContext
import datetime
import jwt
from config import settings
import models as m

class AuthHandler:
    security=HTTPBearer()
    pwd_context=CryptContext(schemes=['bcrypt'])
    secret=settings.TOKEN_SECRET

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, input_password, db_password):
        return self.pwd_context.verify(input_password, db_password)
    
    def encode_token(self, user_id, role_id):
        payload={
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            +datetime.timedelta(minutes=30),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "user_id": user_id,
            "role_id": role_id
        }
        return jwt.encode(payload, self.secret, algorithm=("HS256"))
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=("HS256"))
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Токен просрочен")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Неверный токен")
        
    def auth_wrapper(self, auth:HTTPAuthorizationCredentials=Security(security)):
        return self.decode_token(auth.credentials)
    
    def moderator_wrapper(self, auth:HTTPAuthorizationCredentials=Security(security)):
        payload = self.decode_token(auth.credentials)
        if payload["role_id"] != 3:
            raise HTTPException(403, "Не хватает прав!")
        return payload
    
    def author_wrapper(self, auth:HTTPAuthorizationCredentials=Security(security)):
        payload = self.decode_token(auth.credentials)
        if payload["role_id"] == 1:
            raise HTTPException(403, "Не хватает прав!")
        return payload
    
auth_handler = AuthHandler()
    