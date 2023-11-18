from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer, UserInfoSerializer

# Create your views here.
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def user_profile(request, username):
#     if request.method == 'GET':
#         posts = get_list_or_404(Post)
#         serializer = PostListSerializer(posts, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    if request.user.username == username:
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_info(request, username):
    if request.user.username == username:
        if request.method == 'GET':
            user = get_object_or_404(get_user_model(), username=username)
            serializer = UserInfoSerializer(user)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            serializer = UserInfoSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        