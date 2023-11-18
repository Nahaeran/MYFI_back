from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.user_profile),
    path('<str:username>/info/', views.user_info),
]
