from rest_framework.serializers import BaseSerializer
from rest_framework import serializers
from apps.test.models import ServerTest


class ServerTestSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    isp = serializers.StringRelatedField()

    class Meta:
        model = ServerTest
        fields = ['name', 'country', 'isp', 'ip']
