"""View module for handling requests about game types"""
from tkinter import E
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Subscription, Member
import datetime


class SubscriptionView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def list(self, request):
        subscription = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        follower = Member.objects.get(user=request.auth.user)
        author = Member.objects.get(pk=request.data["author"])

        subscription = Subscription.objects.create(
            follower=follower,
            author=author,
            created=datetime.datetime.now()
        )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def destroy(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'author', 'created')
