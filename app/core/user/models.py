from tortoise import fields, models
from passlib.context import CryptContext
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Scopes(models.Model):
    # manager permission users can

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    users: fields.ManyToManyRelation["Users"] = fields.ManyToManyField(
        "models.Users", related_name="users", through="user_scope"
    )

    class Meta:
        table = "scopes"

    def __str__(self):
        return self.name


class Users(models.Model):
    # user
    id = fields.IntField(pk=True)
    #: This is a email
    name = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255, unique=True)
    verified_hash = fields.CharField(max_length=255, null=True)
    verified_is = fields.BooleanField(default=False)
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    scopes: fields.ManyToManyRelation["Scopes"] = fields.ManyToManyField(
        "models.Scopes", related_name="scopes", through="user_scope"
    )
    
    # events: fields.ManyToManyRelation[Scopes]

    class Meta:
        table = "users"

    def __str__(self):
        return self.name

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
