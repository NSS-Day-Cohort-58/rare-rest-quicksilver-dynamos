from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from operator import itemgetter
from rareserverapi.models import Member
from django.contrib.auth.models import User


class ProfileView(ViewSet):

    def list(self, request):

        profiles = Member.objects.all()
        serialized = ProfileSerializer(profiles, many=True)
        return Response(sorted(serialized.data, key=itemgetter('user["username"]')), status=status.HTTP_200_OK)


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_staff', )

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Member
        fields = ('id', 'bio', 'profile_image_url', 'user', 'full_name', )