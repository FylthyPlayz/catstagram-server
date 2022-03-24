from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from catstagramapi.models import Rating

class RatingView(ViewSet):
    def retrieve(self, request, pk):
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all ratings

        Returns:
            Response -- JSON serialized list of ratings
        """
        rating = Rating.objects.all()
        serializer = RatingSerializer(rating, many=True)
        return Response(serializer.data)

    def create(self, request):
        rating = Rating.objects.create(
            rating=request.data["rating"]
        )
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    def destroy(self, request, pk):
        rating = Rating.objects.get(pk=pk)
        rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        rating = Rating.objects.get(pk=pk)
        rating.label = request.data["rating"]
        rating.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Rating
        fields = ('id', 'rating')