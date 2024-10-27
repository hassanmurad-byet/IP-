# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url_view, name='shorten_url'),
    path('<str:short_key>/', views.redirect_url_view, name='redirect_url'),
]