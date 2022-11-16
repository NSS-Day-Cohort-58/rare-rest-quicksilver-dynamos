from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareserverapi.models import Category
from operator import itemgetter

class CategoryView(ViewSet):

    def list(self, request):

        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(sorted(serialized.data, key=itemgetter('label')), status=status.HTTP_200_OK)

    def create(self, request):

        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk):

        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):

        category = Category.objects.get(pk=pk)
        category.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label', )

class CreateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'label', ]