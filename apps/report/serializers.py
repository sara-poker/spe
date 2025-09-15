from rest_framework.serializers import BaseSerializer
from rest_framework import serializers

from apps.test.models import Isp


class GetAllIspAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Isp
        fields = ['id','name', 'url','isp','org','as_number','asname']
