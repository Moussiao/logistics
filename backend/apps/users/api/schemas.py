from ninja import Schema

from backend.apps.users.models import User


class UserResponse(Schema):
    id: int
    role: User.Role
