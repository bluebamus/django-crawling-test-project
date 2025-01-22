from django.urls import path
from .views import IndexView, BannerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('banner/', BannerView.as_view(), name='banner'),
]