from rest_framework import serializers
from .models import IpModel




class IpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpModel
        fields = ('id', 'ip', 'time')
