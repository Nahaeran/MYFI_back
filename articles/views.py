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


@api_view(['GET'])
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)


# @login_required
# def create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             article = form.save(commit=False)
#             article.user = request.user
#             form.save()
#             return redirect('articles:detail', article.pk)
#     else:
#         form = PostForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'articles/create.html', context)


# @login_required
# def delete(request, pk):
#     article = Post.objects.get(pk=pk)
#     if request.user == article.user:
#         article.delete()
#     return redirect('articles:index')


# @login_required
# def update(request, pk):
#     article = Post.objects.get(pk=pk)
#     if request.user == article.user:
#         if request.method == 'POST':
#             form = PostForm(request.POST, instance=article)
#             if form.is_valid:
#                 form.save()
#                 return redirect('articles:detail', article.pk)
#         else:
#             form = PostForm(instance=article)
#     else:
#         return redirect('articles:index')
#     context = {
#         'article': article,
#         'form': form,
#     }
#     return render(request, 'articles/update.html', context)


# @login_required
# def comments_create(request, pk):
#     article = Post.objects.get(pk=pk)
#     comment_form = CommentForm(request.POST)
#     if comment_form.is_valid():
#         comment = comment_form.save(commit=False)
#         comment.article = article
#         comment.user = request.user
#         comment_form.save()
#         return redirect('articles:detail', article.pk)
#     context = {
#         'article': article,
#         'comment_form': comment_form,
#     }
#     return render(request, 'articles/detail.html', context)


# @login_required
# def comments_delete(request, article_pk, comment_pk):
#     comment = Comment.objects.get(pk=comment_pk)
#     if request.user == comment.user:
#         comment.delete()
#     return redirect('articles:detail', article_pk)

