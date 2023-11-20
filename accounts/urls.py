from django.urls import path
from . import views
from django.urls import path


urlpatterns = [
    path('<str:username>/', views.user_profile),
    path('<str:username>/info/', views.user_info),
    path('<str:username>/profile/', views.user_profile),
] 
