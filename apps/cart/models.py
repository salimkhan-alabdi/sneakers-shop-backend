from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product, Size


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_("Foydalanuvchi")
    )
    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Yangilangan sana"), auto_now=True)

    class Meta:
        verbose_name = _("Savatcha")
        verbose_name_plural = _("Savatchalar")

    def __str__(self):
        return f"{self.user.username} - Savatcha"

    @property
    def total_price(self):
        """Umumiy narx"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Umumiy mahsulotlar soni"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_("Savatcha")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Mahsulot")
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        verbose_name=_("O'lcham")
    )
    quantity = models.PositiveIntegerField(_("Miqdor"), default=1)
    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Yangilangan sana"), auto_now=True)

    class Meta:
        verbose_name = _("Savatcha mahsuloti")
        verbose_name_plural = _("Savatcha mahsulotlari")
        unique_together = ['cart', 'product', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.size.size} x {self.quantity}"

    @property
    def subtotal(self):
        """Mahsulot uchun umumiy narx"""
        return self.product.price * self.quantity