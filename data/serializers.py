from rest_framework import serializers
from .models import ImdbTop250Movies
from django.db.models import fields

class ImdbSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImdbTop250Movies
        fields = ("__all__")


        