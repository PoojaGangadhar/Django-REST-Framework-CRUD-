from django.shortcuts import render
from .models import ImdbTop250Movies
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ImdbSerializers
from django.forms.models import model_to_dict
import json
from rest_framework import status
from rest_framework import serializers
from django.shortcuts import get_object_or_404

# Create your views here.
def retrievingData(request):
    movies = ImdbTop250Movies.objects.all()
    # movieSerializers = ImdbSerializers(movies, many=True)
    return render(request, 'display.html' ,{'movies':movies})


# creating REST API view GET method using serializer
@api_view(['GET'])
def ApiOverview(request):

    """api_urls = {
        'all_items': '/'
    }"""

    movies = ImdbTop250Movies.objects.get(movie_title="The Shawshank Redemption")
    movie_dict = model_to_dict(movies)
    movie_serializer = json.dumps(movie_dict)

    return Response(movie_serializer)


# CRUD Operations Using Serializers
# To create View 
@api_view(['POST'])
def insertData(request):
    values = ImdbSerializers(data=request.data)

    # to validate if data already exist
    if ImdbTop250Movies.objects.filter(**request.data).exists():
        raise serializers.ValidationError("Data already exist")

    if values.is_valid():
        values.save()
        return Response(values.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Django Rest Framework – List View 
@api_view(['GET'])
def viewData(request):

    if request.query_params:
        values = ImdbTop250Movies.objects.filter(**request.query_params.dict())

    else:
        values = ImdbTop250Movies.objects.all()

    if values:
        serializer = ImdbSerializers(values, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# To Update View
@api_view(['POST'])
def updateData(request, pk):
    value = ImdbTop250Movies.objects.get(pk=pk)
    data  = ImdbSerializers(instance=value, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# To delete the records using rest_framework
@api_view(['DELETE'])
def deleteData(request, pk):
    values = get_object_or_404(ImdbTop250Movies, pk=pk)       
    values.delete()
    """value = ImdbTop250Movies.objects.get(pk=pk)
    value.delete()"""
    return Response(status=status.HTTP_202_ACCEPTED)

