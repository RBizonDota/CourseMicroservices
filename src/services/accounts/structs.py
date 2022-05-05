from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel, constr

from accounts.db import User, Token

PydanticToken = sqlalchemy_to_pydantic(Token)

_PydanticUser = sqlalchemy_to_pydantic(User)
class PydanticUser(_PydanticUser):
    def prepare(self):
        self.password = ""

        return self.dict()

class UserCredentials(BaseModel):
    username: constr(max_length=100)
    password: constr(max_length=100)

class ProviderCredentials(BaseModel):
    client_id: constr(max_length=100)
    secret: constr(max_length=100)
    code: constr(max_length=100)

