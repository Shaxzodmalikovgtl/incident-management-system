# incidents/serializers.py
from rest_framework import serializers
from .models import User,Incident

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        exclude = ['incident_id']

    read_only_fields = ['incident_id']


class GetIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
   