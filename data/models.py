from django.db import models

# Create your models here.
class ImdbTop250Movies(models.Model):

    place = models.IntegerField(blank=True, null=True)
    movie_title = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    star_cast = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'imdb_top_250_movies'
