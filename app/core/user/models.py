from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Users(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    #: This is a email
    email = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
    category = fields.CharField(max_length=30, default="misc")
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name or self.family_name:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.email

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]


UserOut = pydantic_model_creator(Users, name="UserOut")
UserPydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

class UserIn(UserPydantic):
    password: str







