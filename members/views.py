from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Member, Performance
from .serializers import MemberSerializer, PerformanceSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
