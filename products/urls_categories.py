from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    # Examples:
    # url(r'^products/', include('products.urls')),
    url(r'^$', CategoryListView.as_view(), name="categories"),
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name="category_detail"),
    # url(r'^(?P<id>\d+)$', 'products.views.product_detail_view', name="product_detail_view"),
]