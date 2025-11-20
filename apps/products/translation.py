from modeltranslation.translator import translator, TranslationOptions

from apps.products.models import Product


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'color', 'material')


translator.register(Product, ProductTranslationOptions)
