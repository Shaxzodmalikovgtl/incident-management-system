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

    # Make sure to include the 'reporter' field here
    read_only_fields = ['incident_id']
