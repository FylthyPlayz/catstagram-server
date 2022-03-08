from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from catstagramapi.models import Post, PostTag, Catstagramer

class PostViewSet(ViewSet):
    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all()
        # posts = Post.objects.order_by('-publication_date')
        tag = PostTag.query_params.get('tag', None)
        if tag is not None:
            posts = posts.filter(tag_id=tag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        catstagramer = Catstagramer.objects.get(user=request.auth.user)
        try:
            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=catstagramer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = CreatePostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        depth = 3

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'publication_date', 'content', 'user', 'tag']