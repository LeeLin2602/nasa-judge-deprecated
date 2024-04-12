from datetime import timezone, datetime
import jwt

class AuthService:
    def __init__(self, logger, jwt_secret, users):
        self.logger = logger
        self.secret = jwt_secret
        self.users = users

    def issue_token(self, profile):
        user = self.users.query_user(profile['email'])
        if not user:
            self.users.add_user(profile['name'], profile['email'])
            user = self.users.query_user(profile['email'])

        now = int(datetime.now(tz=timezone.utc).timestamp())
        payload = {
            "iat": now,
            "exp": now + 3600,
            "uid": user['id'],
            "email": user['email'],
            "role": user['role'],
        }

        token = jwt.encode(payload, self.secret, algorithm="HS256")
        print(token)
        return token

    def authenticate_token(self, payload):
        if not payload:
            raise ValueError("Token is empty")  # More specific exception
        try:
            payload = jwt.decode(payload, self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            self.logger.error(f"Token has expired: {e}")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.error(f"Invalid token: {e}")
            return None

        user = self.users.query_user(payload['email'])
        if not user:
            self.logger.error(f"User not found: {payload['email']}")
            return None
        return user
