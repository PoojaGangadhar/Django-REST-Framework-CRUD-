# Django-REST-Framework-CRUD-
CRUD Operations using Django REST Framework

## IMDB Top 250 Movies Scraping
Using BeautifulSoup for IMDB Top Movies Scraping the results are used as datasets for performing Django REST Framework CRUD Operations
(refer imdbScraping directory for complete code)

from bs4 import BeautifulSoup <br />
import requests <br />
import re <br />
import pandas as pd <br />

url = "https://www.imdb.com/chart/top"  (for imdb website) <br />
response = requests.get(url) <br />
soup = BeautifulSoup(response.text, 'html.parser') <br />
print(soup.prettify()) <br />

## CRUD Operations 
Create django project <br />
    py django-admin startproject dataVisualization <br />
    
Create project app <br />
    py django-admin startapp data <br />
    
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
@api_view(['POST']) <br />
def insertData(request): <br />
    values = ImdbSerializers(data=request.data) <br />
 
    # to validate if data already exist <br />
    if ImdbTop250Movies.objects.filter(**request.data).exists(): <br />
        raise serializers.ValidationError("Data already exist") <br />

    if values.is_valid(): <br />
        values.save() <br /> 
        return Response(values.data) <br />
    else: <br />
        return Response(status=status.HTTP_404_NOT_FOUND) <br />


## Django Rest Framework – List View 
@api_view(['GET']) <br />
def viewData(request): <br />
    if request.query_params: <br />
        values = ImdbTop250Movies.objects.filter(**request.query_params.dict()) <br />

    else: <br />
        values = ImdbTop250Movies.objects.all() <br />

    if values: <br />
        serializer = ImdbSerializers(values, many=True) <br />
        return Response(serializer.data) <br />
    else: <br />
        return Response(status=status.HTTP_404_NOT_FOUND) <br />

## To Update View
@api_view(['POST'])<br />
def updateData(request, pk):<br />
    value = ImdbTop250Movies.objects.get(pk=pk)<br />
    data  = ImdbSerializers(instance=value, data=request.data)<br />

    if data.is_valid():<br />
        data.save()<br />
        return Response(data.data)<br />
    else:<br />
        return Response(status=status.HTTP_404_NOT_FOUND)<br />


## To delete the records using rest_framework
@api_view(['DELETE'])<br />
def deleteData(request, pk):<br />
    values = get_object_or_404(ImdbTop250Movies, pk=pk)    <br />   
    values.delete()<br />
    return Response(status=status.HTTP_202_ACCEPTED)<br />

## In urls.py create the urls for each operations
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
  http://127.0.0.1:8000/topmovies/ <br />
  http://127.0.0.1:8000/apiview/ <br />
  
