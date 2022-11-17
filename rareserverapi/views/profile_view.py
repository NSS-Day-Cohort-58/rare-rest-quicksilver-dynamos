from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from operator import itemgetter
from rareserverapi.models import Member
from django.contrib.auth.models import User


class ProfileView(ViewSet):

    def list(self, request):

        profiles = Member.objects.all().order_by('user__username')
        serialized = ProfileSerializer(profiles, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):

        profile = Member.objects.get(pk=pk)
        serialized = ProfileSerializer(profile, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request, pk):

        if request.auth.user.is_staff:

            profile = Member.objects.get(pk=pk)
            user_id = profile.user_id
            assigned_user = User.objects.get(pk=user_id)
            assigned_user.is_active = request.data['user']['is_active']
            assigned_user.is_staff = request.data['user']['is_staff']
            assigned_user.save()
            
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        else:
            pass


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_staff', 
            'email', 'date_joined', 'username', 'is_active' )

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Member
        fields = ('id', 'bio', 'profile_image_url', 'user', 'full_name', )