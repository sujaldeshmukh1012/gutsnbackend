from views.models import IpModel
from .serializers import IpModelSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class IpModelIndex(APIView):
    def get(self,request,format=None):
        ipModel = IpModel.objects.all()
        serialize = IpModelSerializer(ipModel,many=True)
        return Response(serialize.data)