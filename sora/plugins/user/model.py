from pydantic import BaseModel


class UserToken(BaseModel):
    uid: str
    token: str


class TokenManager:
    def __init__(self):
        self.tokens = {}

    def add_token(self, uid: str, token: str):
        self.tokens[uid] = token

    def remove_token(self, uid: str):
        if uid in self.tokens:
            del self.tokens[uid]

    def update_token(self, uid: str, token: str):
        if uid in self.tokens:
            self.tokens[uid] = token

    def get_token(self, uid: str):
        return self.tokens.get(uid)


class ValidationResult:
    def __init__(self, is_valid: bool, uid: str | None = None):
        self.is_valid = is_valid
        self.uid = uid


def validate_token(token: str) -> ValidationResult:
    for uid, user_token in token_manager.tokens.items():
        if user_token == token:
            return ValidationResult(is_valid=True, uid=uid)
    return ValidationResult(is_valid=False)


token_manager = TokenManager()
