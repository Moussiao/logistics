from ninja import Schema

from apps.users.models import User


class UserResponse(Schema):
    """
    Информация о пользователе, которое отдается по  API.

    Испльзуется Schema, а не ModelSchema, так как ModelSchema не типизирует choices.
    """

    id: int
    role: User.Role
