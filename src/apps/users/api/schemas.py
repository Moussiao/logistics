from ninja import Schema

from src.apps.users.models import User


class UserResponse(Schema):
    id: int
    role: User.Role
