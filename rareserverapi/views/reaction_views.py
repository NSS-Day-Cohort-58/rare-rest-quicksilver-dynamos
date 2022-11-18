"""View module for handling requests about game types"""
from tkinter import E
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Reaction


class ReactionView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)

    def list(self, request):
        reaction = Reaction.objects.all()
        serializer = ReactionSerializer(reaction, many=True)
        return Response(serializer.data)

    def create(self, request):

        reaction = Reaction.objects.create(

            emoji=request.data["emoji"]
        )
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id', 'emoji')
