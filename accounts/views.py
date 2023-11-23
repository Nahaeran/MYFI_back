from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from financial_instruments.models import Deposit, Saving
import json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    if request.user.username == username:
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_info(request, username):
    if request.user.username == username:
        if request.method == 'GET':
            user = get_object_or_404(get_user_model(), username=username)
            serializer = UserInfoSerializer(user)
            return Response(serializer.data)
            
        elif request.method == 'PUT':
            user = get_object_or_404(get_user_model(), username=username)
            serializer = UserInfoSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_info_profile(request, username):
    if request.user.username == username:
        if request.method == 'PUT':
            user = get_object_or_404(get_user_model(), username=username)
            data = { 'profile_img': request.data['profile_img[]']}
            serializer = UserInfoSerializer(instance=user, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# # print('user_data.json')

# with open('accounts/fixtures/accounts/user_data.json', 'r', encoding='UTF8') as f:
#     data = json.loads(f.read())
# # print(data)
# UserModel = get_user_model()

# for user in data:
#     user = user['fields']
#     usertemp = UserModel.objects.create(
#         username=user['username'],
#         name=user['name'],
#         age=user['age'],
#         money=user['money'],
#         salary=user['salary'],
#         password=user['password'],
#         desire_amount_saving=user['desire_amount_saving'],
#         desire_amount_deposit=user['desire_amount_deposit'],
#         deposit_period=user['deposit_period'],
#         saving_period=user['saving_period'],
#         is_active=user['is_active'],
#         is_staff=user['is_staff'],
#         is_superuser=user['is_superuser'],
#     )

#     usertemp.save()

#     for deposit_pk in user['contract_deposit']:
#         deposit = Deposit.objects.get(pk=deposit_pk)
#         deposit.contract_user.add(usertemp)
    
#     for saving_pk in user['contract_saving']:
#         saving = Saving.objects.get(pk=saving_pk)
#         saving.contract_user.add(usertemp)
