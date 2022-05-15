from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from analytics.db import Payment, User

PydanticPayment = sqlalchemy_to_pydantic(Payment)
PydanticUser = sqlalchemy_to_pydantic(User)