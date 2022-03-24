from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from catstagramapi.models import UserRating

class UserRatingView(ViewSet):
    def retrieve(self, request, pk):
        try:
            userrating = UserRating.objects.get(pk=pk)
            serializer = UserRatingSerializer(userrating)
            return Response(serializer.data)
        except UserRating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all ratings

        Returns:
            Response -- JSON serialized list of ratings
        """
        userrating = UserRating.objects.all()
        serializer = UserRatingSerializer(userrating, many=True)
        return Response(serializer.data)

    def create(self, request):
        userrating = UserRating.objects.create(
            userrating=request.data["rating"]
        )
        serializer = UserRatingSerializer(userrating)
        return Response(serializer.data)

    def destroy(self, request, pk):
        rating = UserRating.objects.get(pk=pk)
        rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        userrating = UserRating.objects.get(pk=pk)
        userrating.rating = request.data["rating"]
        userrating.user = request.auth.user
        userrating.post = request.data["post"]
        userrating.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserRatingSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = UserRating
        fields = ('id', 'user', 'post', 'rating')