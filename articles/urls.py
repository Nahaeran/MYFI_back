from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_pk>/', views.post_detail),
    path('', views.post_list),
]
