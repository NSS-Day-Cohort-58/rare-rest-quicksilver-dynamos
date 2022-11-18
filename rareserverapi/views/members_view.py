from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Member
from operator import itemgetter

class MemberView(ViewSet):

    def list(self, request):

        members = Member.objects.all()

        for member in members:
            user = User.objects.get(pk=member.user_id)
            serialized = UserSerializer(user, many=False)
            member.user = user


        serialized = MemberSerializer(members, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        member = Member.objects.get(pk = pk)
        serialized = MemberSerializer(member, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', ]


class MemberSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = Member
        fields = ['id', 'bio', 'profile_image_url', 'user', 'full_name',]