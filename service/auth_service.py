from datetime import timezone, datetime, timedelta
from enum import Enum
import jwt
    
class AuthService:
    def __init__(self, logger, jwt_screct, users):
        self.logger = logger
        self.screct = jwt_screct
        self.users = users

    def issue_token(self, profile):
        user = self.users.query_user(profile['email'])
        if not user:
            self.users.add(profile['name'], profile['email'])
            user = self.users.query(profile['email'])

        now = int(datetime.now(tz=timezone.utc).timestamp())
        payload = {
            "iat": now,
            "exp": now + 3600,
            "uid": user['id'],
            "email": user['email'],
            "role": user['role'],
        }

        token = jwt.encode(payload, self.screct, algorithm="HS256")
        print(token)
        return token

    def authenticate_token(self, payload):
        try:
            if not payload:
                raise Exception("Token is empty")
            try:
                payload = jwt.decode(payload, self.screct, algorithms=["HS256"])
            except Exception as e:
                self.logger.error(f"Failed to decode token: {e}")
                return None
            user = self.users.query_user(payload['email'])
            if not user:
                self.logger.error(f"User not found: {payload['email']}")
                return None
            return user
        except Exception as e:
            self.logger.error(f"Failed to authenticate token: {e}")
            return None