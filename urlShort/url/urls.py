from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('shorten', views.short_url, name="shortURL"),
    path('<str:hash_id>/', views.redirector, name="redirectURL"),
]