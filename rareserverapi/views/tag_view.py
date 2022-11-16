from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Tag
from operator import itemgetter

class TagView(ViewSet):

    def list(self, request):

        tags = Tag.objects.all()
        serialized = TagSerializer(tags, many=True)
        return Response(sorted(serialized.data, key=itemgetter('label')), status=status.HTTP_200_OK)

    def retrieve(self, request, pk):

        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        tag = Tag.objects.get(pk=pk)
        tag.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'label', )
