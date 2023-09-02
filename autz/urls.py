from django.urls import path
from . import views

urlpatterns = [
    path('aut/', views.user_login)
]