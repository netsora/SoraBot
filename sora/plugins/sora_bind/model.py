from pydantic import BaseModel


class UserToken(BaseModel):
    user_id: str
    token: str


class TokenManager:
    def __init__(self):
        self.tokens = {}

    def add_token(self, user_id: str, token: str):
        self.tokens[user_id] = token

    def remove_token(self, user_id: str):
        if user_id in self.tokens:
            del self.tokens[user_id]

    def update_token(self, user_id: str, token: str):
        if user_id in self.tokens:
            self.tokens[user_id] = token

    def get_token(self, user_id: str):
        return self.tokens.get(user_id)


class ValidationResult:
    def __init__(self, is_valid: bool, user_id: str | None = None):
        self.is_valid = is_valid
        self.user_id = user_id


def validate_token(token: str) -> ValidationResult:
    for user_id, user_token in token_manager.tokens.items():
        if user_token == token:
            return ValidationResult(is_valid=True, user_id=user_id)
    return ValidationResult(is_valid=False)


token_manager = TokenManager()
