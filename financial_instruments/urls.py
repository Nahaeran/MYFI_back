from django.urls import path
from . import views


urlpatterns = [
    path('deposit_list/', views.deposit_list),
    path('deposit_list/<str:deposit_code>/', views.deposit_detail),
    path('deposit_list/<str:deposit_code>/Option_list/', views.depositOption_list),
    path('deposit_list/<str:deposit_code>/Option_list/<int:depositOption_pk>/', views.depositOption_detail),
    path('saving_list/', views.saving_list),
    path('saving_list/<str:saving_code>/', views.saving_detail),
    path('saving_list/<str:saving_code>/Option_list/', views.savingOption_list),
    path('saving_list/<str:saving_code>/Option_list/<int:savingOption_pk>/', views.savingOption_detail),
    path('deposit/6months/', views.get_deposits, {'save_trm': '6'}),
    path('deposit/12months/', views.get_deposits, {'save_trm': '12'}),
    path('deposit/24months/', views.get_deposits, {'save_trm': '24'}),
    path('deposit/36months/', views.get_deposits, {'save_trm': '36'}),
    path('saving/6months/', views.get_savings, {'save_trm': '6'}),
    path('saving/12months/', views.get_savings, {'save_trm': '12'}),
    path('saving/24months/', views.get_savings, {'save_trm': '24'}),
    path('saving/36months/', views.get_savings, {'save_trm': '36'}),
    path('deposit/-6months/', views.get_reverse_deposits, {'save_trm': '6'}),
    path('deposit/-12months/', views.get_reverse_deposits, {'save_trm': '12'}),
    path('deposit/-24months/', views.get_reverse_deposits, {'save_trm': '24'}),
    path('deposit/-36months/', views.get_reverse_deposits, {'save_trm': '36'}),
    path('saving/-6months/', views.get_reverse_savings, {'save_trm': '6'}),
    path('saving/-12months/', views.get_reverse_savings, {'save_trm': '12'}),
    path('saving/-24months/', views.get_reverse_savings, {'save_trm': '24'}),
    path('saving/-36months/', views.get_reverse_savings, {'save_trm': '36'}),
    path('deposit_list/<str:deposit_code>/contract/', views.contract_deposit, name='contract_deposit'),
    path('saving_list/<str:saving_code>/contract/', views.contract_saving, name='contract_saving'),
    path('get_bank_deposit/<str:kor_co_nm>/', views.get_bank_deposit),
    path('get_bank_saving/<str:kor_co_nm>/', views.get_bank_saving),
    path('recommend_product_one/', views.recommend_product_one),
    path('recommend_product_two/', views.recommend_product_two),
    path('make_financial_data/', views.make_financial_data)
]
    
