from modeltranslation.translator import translator, TranslationOptions

from apps.brands.models import Brand


class BrandTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Brand, BrandTranslationOptions)