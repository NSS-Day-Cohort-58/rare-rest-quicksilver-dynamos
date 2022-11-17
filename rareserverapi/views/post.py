
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Post, Member, Category, Reaction, Tag, Subscription
from rest_framework.decorators import action



class PostView(ViewSet):

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        subscriptions = Subscription.objects.all()
        posts = Post.objects.all()
        sub = []
        if "author" in request.query_params:
            for post in posts:
                if int(request.query_params['author']) == post.author_id:
                    posts = posts.filter(author=post.author_id)
        if "subscribed" in request.query_params:

            for subscription in subscriptions:

                id = Member.objects.get(
                    user=request.auth.user)
                if subscription.follower_id == id.id:
                    sub.append(subscription)
            if sub:
                for s in sub:

                    posts = posts.filter(author=s.author_id)
            else:
                posts = {}

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):

        category = Category.objects.get(pk=request.data["category"])
        author = Member.objects.get(user=request.auth.user)

        post = Post.objects.create(
            author=author,
            category=category,
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            image_url=request.data["image_url"],
            content=request.data["content"],
            approved=True
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):

        post = Post.objects.get(pk=pk)
        post.author = Member.objects.get(pk=request.data["author"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['post'], detail=True)
    def addTag(self, request, pk):
        """Post request to add a tag to a post"""
    
        tag = Tag.objects.get(pk=request.data["tag_id"])
        post = Post.objects.get(pk=request.data["post_id"])
        post.tags.add(tag)
        return Response({'message': 'Tag added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def removeTag(self, request, pk):
        """delete request to remove a tag from a post"""
    
        tag = Tag.objects.get(pk=request.data["tag_id"])
        post = Post.objects.get(pk=request.data["post_id"])
        post.tags.remove(tag)
        return Response({'message': 'Tag removed'}, status=status.HTTP_204_NO_CONTENT)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'reactions', 'tags')
