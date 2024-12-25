from typing import final

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as StockUserAdmin
from django.utils.translation import gettext_lazy as _

from backend.apps.users.models import User


@final
@admin.register(User)
class UserAdmin(StockUserAdmin[User]):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Персональная информация"),
            {"fields": ("first_name", "last_name", "email", "role")},
        ),
        (
            _("Права доступа"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "role", "password1", "password2"),
            },
        ),
    )
