from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from catstagramapi.models import Catstagramer, Post
from catstagramapi.models.like import Like

class LikeView(ViewSet):
    def retrieve(self, request, pk):
        try:
            like = Like.objects.get(pk=pk)
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        except Like.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all ratings

        Returns:
            Response -- JSON serialized list of ratings
        """
        like = Like.objects.all()
        serializer = LikeSerializer(like, many=True)
        return Response(serializer.data)

    def create(self, request):
        like = Like.objects.create(
            like=request.data["like"]
        )
        serializer = LikeSerializer(like)
        return Response(serializer.data)

    def destroy(self, request, pk):
        like = Like.objects.get(pk=pk)
        like.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        like = Like.objects.get(pk=pk)
        like.like = request.data["like"]
        like.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def like(self, request, pk):
        """Post request for a user to like a post"""
        catstagramer = Catstagramer.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        post.likes.add(catstagramer)
        return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unlike(self, request, pk):
        catstagramer = Catstagramer.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        post.likes.remove(catstagramer)
        return Response({'message': 'Post un-liked'}, status=status.HTTP_204_NO_CONTENT)

class LikeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Like
        fields = ('id', 'user', 'post')