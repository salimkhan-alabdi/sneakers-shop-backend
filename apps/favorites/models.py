from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_("Foydalanuvchi")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name=_("Mahsulot")
    )
    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)

    class Meta:
        verbose_name = _("Sevimli")
        verbose_name_plural = _("Sevimlilar")
        unique_together = ['user', 'product']  # Bir user bir mahsulotni faqat 1 marta qo'sha oladi
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"