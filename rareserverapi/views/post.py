
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Post, Member, Category, Reaction, Tag, Subscription, PostReaction
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
                filteredPosts = []
                for s in sub:
                    for p in posts:
                        if p.author == s.author:
                            filteredPosts.append(p)

                posts = filteredPosts


            else:
                posts = {}



        if "mine" in request.query_params:
            user = Member.objects.get(user=request.auth.user)
            posts = Post.objects.filter(author=user)


        if "search" in request.query_params:
            posts = Post.objects.filter(title__contains=request.query_params['search'])
        else:
            pass
        

        # for post in posts:
        #     author = Member.objects.get(pk=post.author)
        #     post.author=author

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):

        category = Category.objects.get(pk=request.data["category"])
        author = Member.objects.get(user=request.auth.user)

        if request.auth.user.is_staff:
            post = Post.objects.create(
                author=author,
                category=category,
                title=request.data["title"],
                publication_date=request.data["publication_date"],
                image_url=request.data["image_url"],
                content=request.data["content"],
                approved=True
            )
        else:
            post = Post.objects.create(
                author=author,
                category=category,
                title=request.data["title"],
                publication_date=request.data["publication_date"],
                image_url=request.data["image_url"],
                content=request.data["content"],
                approved=False
            )

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):

        author = Member.objects.get(pk=request.auth.user_id)

        post = Post.objects.get(pk=pk)
        post.author = author
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
    def addTags(self, request, pk):
        """Post request to add a tag to a post"""

        post = Post.objects.get(pk=request.data["post_id"])

        postTags = request.data["tags"]

        for postTag in postTags:
            if postTag['isChecked'] == True:
                tag = Tag.objects.get(pk=postTag['id'])
                post.tags.add(tag)

        post.tags.add(tag)
        return Response({'message': 'Tag added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def removeTags(self, request, pk):
        """delete request to remove a tag from a post"""

        post = Post.objects.get(pk=pk)
        post.tags.clear()

        return Response({'message': 'Tag removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def addReaction(self, request, pk):
        """Post request to add a tag to a post"""
        member = Member.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post_id"])
        reaction = Reaction.objects.get(pk=request.data["reaction_id"])
        PostReaction.objects.create(
            member=member,
            post=post,
            reaction=reaction
        )

        return Response({'message': 'Reaction added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def removeReaction(self, request, pk):
        """delete request to remove a tag from a post"""

        reaction = Reaction.objects.get(pk=request.data["reaction_id"])
        post = Post.objects.get(pk=request.data["post_id"])
        post.reactions.remove(reaction)
        return Response({'message': 'Reaction removed'}, status=status.HTTP_204_NO_CONTENT)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'profile_image_url', 'user', 'full_name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label',)


class PostSerializer(serializers.ModelSerializer):

    author = MemberSerializer(many=False)
    category = CategorySerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'reactions', 'tags')
        depth = 1
