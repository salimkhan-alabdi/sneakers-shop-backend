from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(_("Kategoriya nomi"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)

    image_url = models.URLField(_("Rasm URL"), blank=True, null=True)
    image_path = models.CharField(
        _("ImageKit path"),
        max_length=255,
        blank=True,
        null=True,
        help_text="products/42/uuid.jpg"
    )

    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Yangilangan sana"), auto_now=True)

    class Meta:
        verbose_name = _("Kategoriya")
        verbose_name_plural = _("Kategoriyalar")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
