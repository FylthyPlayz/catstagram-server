
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from catstagramapi.models import Catstagramer


class CatstagramerView(ViewSet):
    """Single User View """

    def retrieve(self, request, pk):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user
        """
        try:
            catstagramer = Catstagramer.objects.get(pk=pk)
            serializer = CatstagramerSerializer(catstagramer)
            return Response(serializer.data)
        except Catstagramer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all catstagramers

        Returns:
            Response -- JSON serialized list of catstagramers
        """
        catstagramers = Catstagramer.objects.all()
        # catstagramers = Catstagramer.objects.order_by('-user__username')
        serializer = CatstagramerSerializer(catstagramers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized catstagramer instance
        """
        catstagramer = Catstagramer.objects.get(user=request.auth.user)
        catstagramer.save()
        try:
            serializer = CreateCatstagramerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)      
            return Response(catstagramer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a catstagramer

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            catstagramer = Catstagramer.objects.get(pk=pk)
            user = User.objects.get(pk=pk)
            user.username = request.data["username"]
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]
            catstagramer.bio = request.data["bio"]
            catstagramer.save()
            user.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        catstagramer = Catstagramer.objects.get(pk=pk)
        user = User.objects.get(pk=pk)
        catstagramer.delete()
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)       

class CatstagramerSerializer(serializers.ModelSerializer):
    """JSON serializer for catstagramer
    """
    class Meta:
        model = Catstagramer
        fields = ('id', 'user', 'bio')
        depth = 2
        
class CreateCatstagramerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catstagramer
        fields = ['id', 'user', 'bio']