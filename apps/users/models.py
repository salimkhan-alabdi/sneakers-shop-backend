from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone = models.CharField(_("Telefon"), max_length=13, unique=True, null=True, blank=True)
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    def __str__(self):
        return self.username