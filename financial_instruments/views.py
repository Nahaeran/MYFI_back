from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
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
        Deposit.deposit_set.financial_products.add(deposit.name)
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
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_recommend_list(request):
    '''
    유저의 필요정보
    희망저축금액  desire_amount_deposit 월 200만원 
    희망예치기간  deposit_period 24개월
    가져오고
   
    상품전체를 하나씩 가져오기
    상품을 옵션별(기간별)로 나누기

    최고한도 max_limit
    deposit_set.save_trm 6개월 /12개월 /24개월 /36개월 등 //멀지않게 조정
    같으면 0 같지않으면 차이만큼 -


    기간별 저축금리 = intr_rate

    행렬에 필요정보를 토대로 유저정보를 저장
    상품전체를 행렬에 찍기
    가까운순서대로 10개 뽑아내기
    금리가 높은 순으로 소트하기

    문제점
    적금 희망이 200일때 100짜리 2개를 해도 되고 좀 적게해도되고 좀많이해도된다?
    비교정보 부족?
    가지치기 생각..!
    '''
    
    # print(request.u)
    print(request.user.desire_amount_deposit)
    print(request.user.desire_amount_saving)

    # return Response()
    pass
