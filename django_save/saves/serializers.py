from rest_framework import serializers
from .models import Save


class SaveSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=100)
    # data = serializers.JSONField()

    class Meta:
        model = Save
        fields = '__all__'
