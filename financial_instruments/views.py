from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import F
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import *
from .models import *


# DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={settings.API_KEY}&topFinGrpNo=020000&pageNo=1'
# SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={settings.API_KEY}&topFinGrpNo=020000&pageNo=1'

# deposit_res = requests.get(DEPOSIT_API_URL).json()
# deposit_baseList = deposit_res.get('result').get('baseList')
# deposit_optionList = deposit_res.get('result').get('optionList')

# for base in deposit_baseList:
#     if Deposit.objects.filter(deposit_code=base.get('fin_prdt_cd')):
#         continue
#     save_product = {
#         'deposit_code': base.get('fin_prdt_cd', '-1'),
#         'fin_co_no': base.get('fin_co_no', '-1'),
#         'kor_co_nm': base.get('kor_co_nm', '-1'),
#         'name': base.get('fin_prdt_nm', '-1'),
#         'dcls_month': base.get('dcls_month', '-1'),
#         'mtrt_int': base.get('mtrt_int', '-1'),
#         'etc_note': base.get('etc_note', '-1'),
#         'join_deny': base.get('join_deny', -1),
#         'join_member': base.get('join_member', '-1'),
#         'join_way': base.get('join_way', '-1'),
#         'spcl_cnd': base.get('spcl_cnd', '-1'),
#         'max_limit': base.get('max_limit', -1),
#     }
#     serializer = DepositSerializer(data=save_product)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()

# for option in deposit_optionList:
#     prdt_cd = option.get('fin_prdt_cd', '-1')
#     product = Deposit.objects.get(deposit_code=prdt_cd)
#     save_option = {
#         'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
#         'intr_rate': option.get('intr_rate', -1), # if option.get('intr_rate', -1) else -1,
#         'intr_rate2': option.get('intr_rate2', -1),
#         'save_trm': option.get('save_trm', -1),
#     }

#     serializer = DepositOptionSerializer(data=save_option)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(deposit=product)


# saving_res = requests.get(SAVING_API_URL).json()
# saving_baseList = saving_res.get('result').get('baseList')
# saving_optionList = saving_res.get('result').get('optionList')

# for base in saving_baseList:
#     if Saving.objects.filter(saving_code=base.get('fin_prdt_cd')):
#         continue
#     save_product = {
#         'saving_code': base.get('fin_prdt_cd', '-1'),
#         'fin_co_no': base.get('fin_co_no', '-1'),
#         'kor_co_nm': base.get('kor_co_nm', '-1'),
#         'name': base.get('fin_prdt_nm', '-1'),
#         'dcls_month': base.get('dcls_month', '-1'),
#         'mtrt_int': base.get('mtrt_int', '-1'),
#         'etc_note': base.get('etc_note', '-1'),
#         'join_deny': base.get('join_deny', -1),
#         'join_member': base.get('join_member', '-1'),
#         'join_way': base.get('join_way', '-1'),
#         'spcl_cnd': base.get('spcl_cnd', '-1'),
#         'max_limit': base.get('max_limit', -1),
#     }
#     serializer = SavingSerializer(data=save_product)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()

# for option in saving_optionList:
#     prdt_cd = option.get('fin_prdt_cd', '-1')
#     product = Saving.objects.get(saving_code=prdt_cd)
#     save_option = {
#         'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
#         'rsrv_type_nm': option.get('rsrv_type_nm', '-1'),
#         'intr_rate': option.get('intr_rate', -1), # if option.get('intr_rate', -1) else -1,
#         'intr_rate2': option.get('intr_rate2', -1),
#         'save_trm': option.get('save_trm', -1),
#     }

#     serializer = SavingOptionSerializer(data=save_option)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(saving=product)

@api_view(['GET']) # id 순
def deposit_list(request):
    deposits = Deposit.objects.all()
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_detail(request, deposit_pk):
    deposit = get_object_or_404(Deposit, pk=deposit_pk)
    if request.method == 'GET':
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)    
    

@api_view(['GET'])
def depositOption_list(request, deposit_pk):
    deposit = get_object_or_404(Deposit, pk=deposit_pk)
    deposit_options = DepositOption.objects.filter(deposit=deposit)

    if request.method == 'GET':
        serializer = DepositOptionSerializer(deposit_options, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def depositOption_detail(request, deposit_pk, depositOption_pk):
    deposit = get_object_or_404(Deposit, pk=deposit_pk)
    deposit_option = get_object_or_404(DepositOption, pk=depositOption_pk, deposit=deposit)

    if request.method == 'GET':
        serializer = DepositOptionSerializer(deposit_option)
        return Response(serializer.data)
    

@api_view(['GET']) # id 순
def saving_list(request):
    savings = Saving.objects.all()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def saving_detail(request, saving_pk):
    saving = get_object_or_404(Saving, pk=saving_pk)
    if request.method == 'GET':
        serializer = SavingSerializer(saving)
        return Response(serializer.data)

    
@api_view(['GET'])
def savingOption_list(request, saving_pk):
    saving = get_object_or_404(Saving, pk=saving_pk)
    saving_options = SavingOption.objects.filter(saving=saving)

    if request.method == 'GET':
        serializer = SavingOptionSerializer(saving_options, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def savingOption_detail(request, saving_pk, savingOption_pk):
    savingOption = get_object_or_404(SavingOption, pk=savingOption_pk)
    if request.method == 'GET':
        serializer = SavingOptionSerializer(savingOption)
        return Response(serializer.data)
    

# 6개월~36개월
@api_view(['GET'])
def get_deposits(request, save_trm):
    deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('depositoption__intr_rate')

    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_savings(request, save_trm):
    savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('savingoption__intr_rate')

    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_reverse_deposits(request, save_trm):
    deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('-depositoption__intr_rate')

    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_reverse_savings(request, save_trm):
    savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('-savingoption__intr_rate')

    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

