import base64
import uuid
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from catstagramapi.models import Post, Catstagramer, Tag

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
        # tag = PostTag.query_params.get('tag', None)
        # if tag is not None:
        #     posts = posts.filter(tag_id=tag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        catstagramer = Catstagramer.objects.get(user=request.auth.user)
        tags = []
        for tag in request.data['tags']:
            tags.append(Tag.objects.get(pk=tag))
        try:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
            name=f'media/{catstagramer.user.username}-{uuid.uuid4()}.{ext}')
            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=catstagramer, image=data, tags=tags)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            catstagramer = Catstagramer.objects.get(user=request.auth.user)
            post = Post.objects.get(pk=pk)
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), 
            name=f'media/{catstagramer.user.username}-{uuid.uuid4()}.{ext}')
            serializer = CreatePostSerializer(post, data=request.data)
            # post.post_image = data
            serializer.is_valid(raise_exception=True)
            post = serializer.save(user=catstagramer, image=data)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # @action(methods=['post'], detail=True)
    # def like(self, request, pk):
    #     """Post request for a user to sign up for an event"""
    #     catstagramer = Catstagramer.objects.get(user=request.auth.user)
    #     post = Post.objects.get(pk=pk)
    #     post.like.add(catstagramer)
    #     return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)

    # @action(methods=['delete'], detail=True)
    # def unlike(self, request, pk):
    #     catstagramer = Catstagramer.objects.get(user=request.auth.user)
    #     post = Post.objects.get(pk=pk)
    #     post.like.remove(catstagramer)
    #     return Response({'message': 'Post un-liked'}, status=status.HTTP_204_NO_CONTENT)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        depth = 3

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'publication_date', 'content', 'user']
        