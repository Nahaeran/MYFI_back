from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import PostListSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment


# Create your views here.
# 전체 게시글 조회 및 게시글 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = get_list_or_404(Post)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#단일 게시글 조회,삭제 및 수정 및 조회
@api_view(['GET','PUT','DELETE'])
def post_detail(request, post_pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            post = get_object_or_404(Post, pk=post_pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            post = get_object_or_404(Post, pk=post_pk)
            if request.user == post.user:
                post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'PUT':
            post = get_object_or_404(Post, pk=post_pk)
            serializer = PostSerializer(instance=post, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        
       
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def comment_list(request,post_pk):
    post = get_object_or_404(Post,pk=post_pk)

    if request.method=='GET':
        comments = post.comment_set.all()
        serializer=CommentSerializer(comments,many=True)
        return Response(serializer.data)
    
    elif request.method=="POST":
        serializer = CommentSerializer(data=request.data) #1
        if serializer.is_valid(raise_exception=True): #2
            serializer.save(post=post) 
        return Response(serializer.data,status=status.HTTP_201_CREATED)


#단일 댓글 조회,삭제 및 수정 및 조회
@api_view(['GET','PUT','DELETE'])
def comment_detail(request, post_pk, comment_pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            comment = get_object_or_404(Comment, pk=comment_pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            comment = get_object_or_404(Comment, pk=comment_pk)
            if request.user == comment.user:
                comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'PUT':
            comment = get_object_or_404(Comment, pk=comment_pk)
            serializer = CommentSerializer(instance=comment, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

    





    

            

                



