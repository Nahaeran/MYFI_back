from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import User
import requests
from .serializers import *
from .models import *


# DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={settings.BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'
# SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={settings.BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'

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
def deposit_detail(request, deposit_code):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
    if request.method == 'GET':
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)    
    

@api_view(['GET'])
def depositOption_list(request, deposit_code):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
    deposit_options = DepositOption.objects.filter(deposit=deposit)

    if request.method == 'GET':
        serializer = DepositOptionSerializer(deposit_options, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def depositOption_detail(request, deposit_code, depositOption_pk):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
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
def saving_detail(request, saving_code):
    saving = get_object_or_404(Saving, saving_code=saving_code)
    if request.method == 'GET':
        serializer = SavingSerializer(saving)
        return Response(serializer.data)

    
@api_view(['GET'])
def savingOption_list(request, saving_code):
    saving = get_object_or_404(Saving, saving_code=saving_code)
    saving_options = SavingOption.objects.filter(saving=saving)

    if request.method == 'GET':
        serializer = SavingOptionSerializer(saving_options, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def savingOption_detail(request, saving_code, savingOption_pk):
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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def contract_deposit(request, deposit_code):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
    if request.user in deposit.contract_user.all():
        deposit.contract_user.remove(request.user)
    else:
        deposit.contract_user.add(request.user)
    serializer = ContractDepositSerializer(deposit)
    return Response(serializer.data)


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def contract_deposit(request, deposit_code):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
    if request.method == 'GET':
        serializer = ContractDepositSerializer(deposit)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user in deposit.contract_user.all():
            deposit.contract_user.remove(request.user)
            return Response({ "detail": "삭제되었습니다." }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "detail": "삭제할 항목이 없습니다." }, status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'POST':
        if request.user not in deposit.contract_user.all():
            deposit.contract_user.add(request.user)
            serializer = ContractDepositSerializer(deposit, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({ "detail": "상품이 추가되었습니다." }, status=status.HTTP_200_OK)
        else:
            return Response({ "detail": "이미 상품이 존재합니다." }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def contract_saving(request, saving_code):
    saving = get_object_or_404(Saving, saving_code=saving_code)
    if request.method == 'GET':
        serializer = ContractSavingSerializer(saving)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user in saving.contract_user.all():
            saving.contract_user.remove(request.user)
            return Response({ "detail": "삭제되었습니다." }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "detail": "삭제할 항목이 없습니다." }, status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'POST':
        if request.user not in saving.contract_user.all():
            saving.contract_user.add(request.user)
            serializer = ContractSavingSerializer(saving, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({ "detail": "상품이 추가되었습니다." }, status=status.HTTP_200_OK)
        else:
            return Response({ "detail": "이미 상품이 존재합니다." }, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_bank_deposit(request, kor_co_nm):
    if Deposit.objects.filter(kor_co_nm=kor_co_nm).exists():
        deposits = Deposit.objects.filter(kor_co_nm=kor_co_nm)
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)
    else:
        return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_bank_saving(request, kor_co_nm):
    if Saving.objects.filter(kor_co_nm=kor_co_nm).exists():
        savings = Saving.objects.filter(kor_co_nm=kor_co_nm)
        serializer = SavingSerializer(savings, many=True)
        return Response(serializer.data)
    else:
        return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET']) #예금
@permission_classes([IsAuthenticated])
def deposit_recommend_list(request):
    user = get_object_or_404(User, username=request.user.username)
    desired_amount = user.desire_amount_deposit #유저의 희망금액
    desired_period = user.deposit_period    #유저의 희망 기간
   
    if not desired_period or not desired_amount:
        if not desired_period:
            return Response({"message": "유저의 희망예금이 없습니다."})
        elif not desired_amount:
            return Response({"message": "유저의 희망예금금액이 없습니다."})

    desired_period = int(desired_period)
    desired_amount = int(desired_amount)

    deposit_options = DepositOption.objects.filter(
        save_trm__in=[6, 12, 24, 36]
    )
    deposit_options = deposit_options.order_by("save_trm")
    deposit_options = deposit_options.order_by("deposit__max_limit")

    deposit_options = deposit_options.filter(
        save_trm__lte=desired_period + desired_period//2, #상품의 기간이 유저의 희망기간보다 낮은것들
        deposit__max_limit__gte=desired_amount - desired_amount//2,  # 상품의 적금한도가 유저의 희망보다 높은것들
    )

    deposit_options = deposit_options.order_by("-intr_rate") #-가 높은순으로 나옴
    deposit_options = deposit_options[:10]


    serializers = DepositOptionSerializer2(deposit_options, many=True)

    return Response(serializers.data)


@api_view(['GET']) #적금
@permission_classes([IsAuthenticated])
def saving_recommend_list(request):
    user = get_object_or_404(User, username=request.user.username)
    desired_amount = user.desire_amount_saving #유저의 희망금액
    desired_period = user.saving_period    #유저의 희망 기간
   
    if not desired_period or not desired_amount:
        if not desired_period:
            return Response({"message": "유저의 희망기간이 없습니다."})
        elif not desired_amount:
            return Response({"message": "유저의 희망적금금액이 없습니다."})

    desired_period = int(desired_period)
    desired_amount = int(desired_amount)

    saving_options = SavingOption.objects.filter(
        save_trm__in=[6, 12, 24, 36]
    )
    saving_options = saving_options.order_by("save_trm")
    saving_options = saving_options.order_by("saving__max_limit")

    deposit_options = deposit_options.filter(
        save_trm__lte=desired_period + desired_period//2, #상품의 기간이 유저의 희망기간보다 낮은것들
        saving__max_limit__gte=desired_amount - desired_amount//2,  # 상품의 적금한도가 유저의 희망보다 높은것들
    )

    saving_options = saving_options.order_by("-intr_rate") #-가 높은순으로 나옴
    saving_options = saving_options[:10]


    serializers = SavingOptionSerializer2(saving_options, many=True)

    return Response(serializers.data)
