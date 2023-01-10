from django.db.models import fields
from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Person
		fields = ('documentType', 
        'documentNumber', 
        'first_name', 
        'second_name', 
        'lastName', 
        'hobbie')

class SearchPerson(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('documentType', 
        'documentNumber')