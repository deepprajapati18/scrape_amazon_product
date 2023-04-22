from django.urls import path

from products.views import ScrapeProductsView

urlpatterns = [
    path(
        'scrape-products/',
        ScrapeProductsView.as_view(),
        name='scrape-products',
    )
]
