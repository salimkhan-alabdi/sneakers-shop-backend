from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.brands.models import Brand


@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}