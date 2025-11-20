from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(_("Brand nomi"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    created_at = models.DateTimeField(_("Yaratilgan sana"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Yangilangan sana"), auto_now=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brandlar")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)