import base64
import uuid
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
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
        posts = Post.objects.order_by('-publication_date')
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
            tags = []
            for tag in request.data['tags']:
                tags.append(Tag.objects.get(pk=tag))
            serializer = CreatePostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            if request.data["image"]: 
                format, imgstr = request.data["image"].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), 
                name=f'media/{catstagramer.user.username}-{uuid.uuid4()}.{ext}')
                post = serializer.save(user=catstagramer, image=data, tags=tags)
            else: 
                serializer.save(user=catstagramer, tags=tags)
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
        fields = ['id', 'publication_date', 'content', 'user']
        