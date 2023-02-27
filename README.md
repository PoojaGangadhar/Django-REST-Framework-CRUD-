# Django-REST-Framework-CRUD-
CRUD Operations using Django REST Framework

## IMDB Top 250 Movies Scraping
Using BeautifulSoup for IMDB Top Movies Scraping the results are used as datasets for performing Django REST Framework CRUD Operations
(refer imdbScraping directory for complete code)

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = "https://www.imdb.com/chart/top"  (for imdb website)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())

## CRUD Operations 
Create django project 
    py django-admin startproject dataVisualization
    
Create project app
    py django-admin startapp data
    
Create the following model class in models.py

    class ImdbTop250Movies(models.Model):
    place = models.IntegerField(blank=True, null=True)
    movie_title = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    star_cast = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'imdb_top_250_movies'

In django app create serializer class as below in serializers.py
     
     class ImdbSerializers(serializers.ModelSerializer):
        class Meta:
          model = ImdbTop250Movies
          fields = ("__all__")

Refer views.py for GET, PUT, POST and DELETE operations
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
    return Response(status=status.HTTP_202_ACCEPTED)

# In urls.py create the urls for each operations
    urlpatterns = [
    path("admin/", admin.site.urls),
    path("topmovies/", views.retrievingData),   # to view all records in html page
    path("apiview/", views.ApiOverview),        # example viewset for rest_framework
    path("create/", views.insertData, name="insertData"),      # create data using rest_framework
    path("all/", views.viewData, name="viewData"),    # view data using rest_framework
    path("update/<int:pk>/", views.updateData, name='updateData'), # update data using rest_framework
    path("delete/<int:pk>/", views.deleteData, name='deleteData'), # delete data using rest_framework
    ]

## To run server use following command
  py manage.py runserver
  
## To see the results use urls like shown below
  http://127.0.0.1:8000/topmovies/
  http://127.0.0.1:8000/apiview/
  
