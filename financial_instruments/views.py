from collections import Counter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import User
import requests
from .serializers import *
from .models import *
from accounts.serializers import *

def make_financial_data(request):
    DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={settings.BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'
    SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={settings.BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'

    deposit_res = requests.get(DEPOSIT_API_URL).json()
    deposit_baseList = deposit_res.get('result').get('baseList')
    deposit_optionList = deposit_res.get('result').get('optionList')

    for base in deposit_baseList:
        if Deposit.objects.filter(deposit_code=base.get('fin_prdt_cd')):
            continue
        save_product = {
            'deposit_code': base.get('fin_prdt_cd', '-1'),
            'fin_co_no': base.get('fin_co_no', '-1'),
            'kor_co_nm': base.get('kor_co_nm', '-1'),
            'name': base.get('fin_prdt_nm', '-1'),
            'dcls_month': base.get('dcls_month', '-1'),
            'mtrt_int': base.get('mtrt_int', '-1'),
            'etc_note': base.get('etc_note', '-1'),
            'join_deny': base.get('join_deny', -1),
            'join_member': base.get('join_member', '-1'),
            'join_way': base.get('join_way', '-1'),
            'spcl_cnd': base.get('spcl_cnd', '-1'),
            'max_limit': base.get('max_limit', -1),
        }
        serializer = DepositSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option in deposit_optionList:
        prdt_cd = option.get('fin_prdt_cd', '-1')
        product = Deposit.objects.get(deposit_code=prdt_cd)
        save_option = {
            'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
            'intr_rate': option.get('intr_rate', -1), # if option.get('intr_rate', -1) else -1,
            'intr_rate2': option.get('intr_rate2', -1),
            'save_trm': option.get('save_trm', -1),
        }

        serializer = DepositOptionSerializer(data=save_option)
        if serializer.is_valid(raise_exception=True):
            serializer.save(deposit=product)


    saving_res = requests.get(SAVING_API_URL).json()
    saving_baseList = saving_res.get('result').get('baseList')
    saving_optionList = saving_res.get('result').get('optionList')

    for base in saving_baseList:
        if Saving.objects.filter(saving_code=base.get('fin_prdt_cd')):
            continue
        save_product = {
            'saving_code': base.get('fin_prdt_cd', '-1'),
            'fin_co_no': base.get('fin_co_no', '-1'),
            'kor_co_nm': base.get('kor_co_nm', '-1'),
            'name': base.get('fin_prdt_nm', '-1'),
            'dcls_month': base.get('dcls_month', '-1'),
            'mtrt_int': base.get('mtrt_int', '-1'),
            'etc_note': base.get('etc_note', '-1'),
            'join_deny': base.get('join_deny', -1),
            'join_member': base.get('join_member', '-1'),
            'join_way': base.get('join_way', '-1'),
            'spcl_cnd': base.get('spcl_cnd', '-1'),
            'max_limit': base.get('max_limit', -1),
        }
        serializer = SavingSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option in saving_optionList:
        prdt_cd = option.get('fin_prdt_cd', '-1')
        product = Saving.objects.get(saving_code=prdt_cd)
        save_option = {
            'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
            'rsrv_type_nm': option.get('rsrv_type_nm', '-1'),
            'intr_rate': option.get('intr_rate', -1), # if option.get('intr_rate', -1) else -1,
            'intr_rate2': option.get('intr_rate2', -1),
            'save_trm': option.get('save_trm', -1),
        }

        serializer = SavingOptionSerializer(data=save_option)
        if serializer.is_valid(raise_exception=True):
            serializer.save(saving=product)
    return HttpResponse("금융 데이터 생성 완료")

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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_product_one(request):
    user = get_object_or_404(User, username=request.user.username)
    desired_amount_deposit = user.desire_amount_deposit
    desired_period_deposit = user.deposit_period

    if not desired_period_deposit or not desired_amount_deposit:
        if not desired_period_deposit:
            return Response({"message": "유저의 희망기간이 없습니다."})
        elif not desired_amount_deposit:
            return Response({"message": "유저의 희망적금금액이 없습니다."})

    # Convert desired_period_deposit and desired_amount_deposit to integers
    desired_period_deposit = int(desired_period_deposit)
    desired_amount_deposit = int(desired_amount_deposit)

    # Filter deposit options
    # deposit_options = DepositOption.objects.filter(
    #     save_trm__in=[6, 12, 24, 36]
    # )
    # deposit_options = deposit_options.order_by("save_trm")
    # deposit_options = deposit_options.order_by("deposit__max_limit")

    # # Handle null values for max_limit
    # deposit_options = deposit_options.filter(
    #     Q(deposit__max_limit__gte=desired_amount_deposit - desired_amount_deposit // 2) | Q(deposit__max_limit__isnull=True)
    # )

    # # Filter deposit options by desired period
    # deposit_options = deposit_options.filter(
    #     save_trm__lte=desired_period_deposit + desired_period_deposit // 2
    # )

    # # Sort deposit options by interest rate and limit to top 10
    # deposit_options = deposit_options.order_by("-intr_rate")
    # deposit_options = deposit_options[:10]

    deposit = Deposit.objects.filter(
        Q(max_limit__gte=desired_amount_deposit - desired_amount_deposit // 2) | Q(max_limit__isnull=True)
    )

    deposit = deposit.filter(
        depositoption__save_trm__lte=desired_period_deposit + desired_period_deposit // 2
    )
    
    deposit = list(set(deposit.order_by("-depositoption__intr_rate")[:10]))
    # deposit = deposit[:10]

    ####### saving

    desired_amount_saving = user.desire_amount_saving
    desired_period_saving = user.saving_period

    # Filter saving options
    # saving_options = SavingOption.objects.filter(
    #     save_trm__in=[6, 12, 24, 36]
    # )
    # saving_options = saving_options.order_by("save_trm")
    # saving_options = saving_options.order_by("saving__max_limit")

    # # Handle null values for max_limit
    # saving_options = saving_options.filter(
    #     Q(saving__max_limit__gte=desired_amount_saving - desired_amount_saving // 2) | Q(saving__max_limit__isnull=True)
    # )

    # # Filter saving options by desired period
    # saving_options = saving_options.filter(
    #     save_trm__lte=desired_period_saving + desired_period_saving // 2
    # )

    # # Sort saving options by interest rate and limit to top 10
    # saving_options = saving_options.order_by("-intr_rate")
    # saving_options = saving_options[:10]

    # Serialize deposit and saving options
    # depositserializers = DepositOptionSerializer2(deposit_options, many=True)
    # savingserializers = SavingOptionSerializer2(saving_options, many=True)

    saving = Saving.objects.filter(
        Q(max_limit__gte=desired_amount_saving - desired_amount_saving // 2) | Q(max_limit__isnull=True)
    )

    saving = saving.filter(
        savingoption__save_trm__lte=desired_period_saving + desired_period_saving // 2
    )

    saving = list(set(saving.order_by("-savingoption__intr_rate")[:10]))
    # saving = saving[:10]

    depositserializers = DepositSerializer(deposit, many=True)
    savingserializers = SavingSerializer(saving, many=True)

    # Create response data
    product_list = {
        "deposit": depositserializers.data,
        "saving": savingserializers.data,
    }

    return Response(product_list)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_product_two(request): 
    age = request.user.age
    money = request.user.money
    salary = request.user.salary
    standard_deviation_age = 6
    standard_deviation_money = 1000000
    standard_deviation_salary = 1000000
    is_not_similar_users = False

    similar_users = User.objects.filter(
        ~Q(username=request.user.username),
        age__range=(age - standard_deviation_age, age + standard_deviation_age),
        money__range=(money - standard_deviation_money, money + standard_deviation_money),
        salary__range=(salary - standard_deviation_salary, salary + standard_deviation_salary)
    )

    if not similar_users.exists():
        is_not_similar_users = True
        similar_users = User.objects.all()

    id_data = []

    for similar_user in similar_users:
        serializer = UserInfoSerializer(similar_user)
        id_data.append(serializer.data["id"])

    # print(len(id_data))

    deposit_list = []
    saving_list = []
    
    for user_id in id_data:
        user = User.objects.get(pk=user_id)
        deposit_list.extend(user.contract_deposit.all())
        saving_list.extend(user.contract_saving.all())

    # Counter를 사용하여 각 Deposit과 Saving 객체의 등장 횟수를 계산
    deposit_counter = Counter(deposit_list)
    saving_counter = Counter(saving_list)


    # 각 객체와 그 등장 횟수를 저장할 리스트
    deposit_result = []
    saving_result = []

    for deposit, count in deposit_counter.items():
        # Deposit 객체의 정보와 등장 횟수를 딕셔너리로 저장
        deposit_info = {'deposit': DepositSerializer(deposit).data, 'count': count}
        deposit_result.append(deposit_info)

    for saving, count in saving_counter.items():
        # Saving 객체의 정보와 등장 횟수를 딕셔너리로 저장
        saving_info = {'saving': SavingSerializer(saving).data, 'count': count}
        saving_result.append(saving_info)

    # 등장 횟수를 기준으로 내림차순 정렬
    deposit_result = sorted(deposit_result, key=lambda x: x['count'], reverse=True)[:10]
    saving_result = sorted(saving_result, key=lambda x: x['count'], reverse=True)[:10]

    result = {'is_not_similar_users': is_not_similar_users, 'deposit': deposit_result, 'saving': saving_result}

    return Response(result)

