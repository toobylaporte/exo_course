from rest_framework import serializers
from .models import Member, Performance

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class PerformanceSerializer(serializers.ModelSerializer):
    # member = serializers.StringRelatedField()  # Affiche le nom du membre
    class Meta:
        model = Performance
        fields = '__all__'
