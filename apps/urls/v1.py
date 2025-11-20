from django.urls import path, include

urlpatterns = [
    path('products/', include('apps.products.urls.v1', namespace='products')),
    path('categories/', include('apps.categories.urls.v1', namespace='categories')),
    path('brands/', include('apps.brands.urls.v1', namespace='brands'))
]
