from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from .serializers import PostListSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        # 페이지 네이션 설정
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 표시할 게시글 수를 조정
        
        posts = Post.objects.all().order_by('-created_at')  # created_at 역순으로 정렬(최신)
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ "detail": "Authentication credentials were not provided." }, status=status.HTTP_401_UNAUTHORIZED)



#단일 게시글 조회,삭제 및 수정 및 조회
@api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticated])
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            if request.user == post.user:
                post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "detail": "Authentication credentials were not provided." }, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        if request.user.is_authenticated:
            serializer = PostSerializer(instance=post, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({ "detail": "Authentication credentials were not provided." }, status=status.HTTP_401_UNAUTHORIZED)

            
#사용자 이름에 해당하는 사용자의 포스트 목록 조회
@api_view(['GET'])
def user_post_list(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    user_posts = user.post_set.all()
    serializer = PostSerializer(user_posts, many=True)
    return Response(serializer.data)
        
       
@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def comment_list(request, post_pk):
    post = get_object_or_404(Post,pk=post_pk)
    
    if request.method=='GET':
        comments = post.comment_set.all()
        serializer=CommentSerializer(comments,many=True)
        return Response(serializer.data)
    
    elif request.method=="POST":
        if request.user.is_authenticated:
            serializer = CommentSerializer(data=request.data) #1
            if serializer.is_valid(raise_exception=True): #2
                serializer.save(post=post, user=request.user) 
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({ "detail": "Authentication credentials were not provided." }, status=status.HTTP_401_UNAUTHORIZED)


#단일 댓글 조회,삭제 및 수정 및 조회
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "detail": "댓글 작성자와 사용자가 다릅니다." }, status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'PUT':
        if request.user == comment.user:
            serializer = CommentSerializer(instance=comment, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({ "detail": "댓글 작성자와 사용자가 다릅니다."}, status=status.HTTP_401_UNAUTHORIZED)


