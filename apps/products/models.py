from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.utils.crypto import get_random_string

from apps.brands.models import Brand
from apps.categories.models import Category


class Product(models.Model):
    GENDER_CHOICES = [
        ("male", _("Erkak")),
        ("female", _("Ayol")),
    ]

    name = models.CharField(_("Mahsulot nomi"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Kategoriya"),
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Brand"),
    )

    price = models.DecimalField(
        _("Narx"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )

    gender = models.CharField(
        _("Jins"),
        max_length=10,
        choices=GENDER_CHOICES,
    )

    color_hex = models.CharField(
        _("Rang HEX kodi"),
        max_length=7,
        validators=[
            RegexValidator(
                regex=r"^#[0-9A-Fa-f]{6}$",
                message="HEX rang #FFFFFF formatida bo‘lishi kerak",
            )
        ],
    )

    material = models.CharField(_("Material"), max_length=100)

    is_popular = models.BooleanField(_("Mashhur"), default=False)
    is_new = models.BooleanField(_("Yangi"), default=False)

    rating = models.FloatField(
        _("Reyting"),
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Yangilangan sana"), auto_now=True)

    class Meta:
        verbose_name = _("Mahsulot")
        verbose_name_plural = _("Mahsulotlar")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Mahsulot"),
    )

    image_url = models.URLField(_("Rasm URL"), blank=True, null=True)
    image_path = models.CharField(
        _("ImageKit path"),
        max_length=255,
        blank=True,
        null=True,
        help_text="products/42/uuid.jpg",
    )

    is_main = models.BooleanField(_("Asosiy rasm"), default=False)
    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)

    class Meta:
        verbose_name = _("Mahsulot rasmi")
        verbose_name_plural = _("Mahsulot rasmlari")
        ordering = ["-is_main", "-created_at"]

    def __str__(self):
        return f"{self.product.name} - image"

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product,
                is_main=True,
            ).update(is_main=False)
        super().save(*args, **kwargs)


class Size(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sizes",
        verbose_name=_("Mahsulot"),
    )

    size = models.CharField(_("O'lcham"), max_length=10)
    stock = models.PositiveIntegerField(_("Qoldiq"), default=0)

    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Yangilangan sana"), auto_now=True)

    class Meta:
        verbose_name = _("O'lcham")
        verbose_name_plural = _("O'lchamlar")
        unique_together = ["product", "size"]
        ordering = ["size"]

    def __str__(self):
        return f"{self.product.name} - {self.size}"
