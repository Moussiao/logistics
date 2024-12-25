from typing import final

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


@final
class TgUserChat(models.Model):
    user = models.ForeignKey(
        to="tg_bots.TgUser",
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="links_to_chats",
    )
    chat = models.ForeignKey(
        to="tg_bots.TgChat",
        verbose_name=_("Чат"),
        on_delete=models.PROTECT,
        related_name="links_to_users",
    )

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta(TypedModelMeta):
        verbose_name = _("Связь пользователя с чатом")
        verbose_name_plural = _("Связи пользователей с чатами")

    def __str__(self) -> str:
        return f"{self.user_id=} -> {self.chat_id=}"
