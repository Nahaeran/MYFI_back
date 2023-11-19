from django.urls import path
from . import views


urlpatterns = [
    path('deposit_list/', views.deposit_list),
    path('deposit_list/<int:deposit_pk>/', views.deposit_detail),
    path('deposit_list/<int:deposit_pk>/Option_list/', views.depositOption_list),
    path('deposit_list/<int:deposit_pk>/Option_list/<int:depositOption_pk>/', views.depositOption_detail),
    path('saving_list/', views.saving_list),
    path('saving_list/<int:saving_pk>/', views.saving_detail),
    path('saving_list/<int:saving_pk>/Option_list/', views.savingOption_list),
    path('saving_list/<int:saving_pk>/Option_list/<int:savingOption_pk>/', views.savingOption_detail),
]
    
