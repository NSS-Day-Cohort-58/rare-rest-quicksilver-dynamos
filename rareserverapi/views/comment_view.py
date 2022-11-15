from dataclasses import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Comment

class CommentView(ViewSet):

    def list(self, requst):

        comments = Comment.objects.all()
        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):

        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk):

        comment = Comment.objects.get(pk=pk)
        comment.subject = request.data["subject"]
        comment.content = request.data["content"]
        comment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'subject', 'created', ]

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'subject', 'created', ]