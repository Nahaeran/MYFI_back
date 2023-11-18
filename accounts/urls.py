from django.urls import path
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<str:username>/', views.user_profile),
    path('<str:username>/info/', views.user_info),
] 
