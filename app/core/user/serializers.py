from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from app.core.user.models import Users, Scopes

UserOut = pydantic_model_creator(Users, name="UserOut")
UserOutList = pydantic_queryset_creator(Users, name="UserOut")
UserPydantic = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True)
ScopeFull = pydantic_model_creator(Scopes)
Scope_List = pydantic_queryset_creator(Scopes)


class UserIn(UserPydantic):
    password: str
