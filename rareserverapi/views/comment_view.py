from dataclasses import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Comment, Post, Member
import datetime

class CommentView(ViewSet):

    def list(self, request):

        comments = Comment.objects.all()
        filteredComments = []
        if "postId" in request.query_params:
            for comment in comments:
                if int(request.query_params['postId']) == comment.post_id:
                    filteredComments.append(comment)
            serialized = CommentSerializer(filteredComments, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
                    
        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):

        post = Post.objects.get(pk=request.data["post_id"])
        author = Member.objects.get(user=request.auth.user)

        comment = Comment.objects.create(
            author = author,
            post = post,
            content = request.data["content"],
            subject = request.data["subject"],
            created = datetime.date.today()
        )


        serializer = CreateCommentSerializer(comment)
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