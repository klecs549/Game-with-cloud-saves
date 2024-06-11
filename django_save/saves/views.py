from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.http import HttpRequest

from .models import Save
from .serializers import SaveSerializer
# Create your views here.


class SaveViews(generics.CreateAPIView):
    request = HttpRequest()
    if request.method == 'GET':
        print(request.GET)
    queryset = Save.objects.all()
    serializer_class = SaveSerializer
    # def perform_create(self, serializer):
    #     return super().perform_create()


class GetSaveViews(generics.ListAPIView):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer

