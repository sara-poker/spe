from rest_framework.serializers import BaseSerializer
from rest_framework import serializers
from apps.test.models import ServerTest , SpeedTest


class ServerTestSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    isp = serializers.StringRelatedField()

    class Meta:
        model = ServerTest
        fields = ['id','name', 'country', 'isp', 'url', 'ip']



class AddRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedTest
        fields = [
            "id",
            "user",
            "network_info",
            "device_info",
            "server_test",
            "ping_avg",
            "jitter",
            "packet_loss",
            "speed_mbps",
            "loaded_size",
            "load_time",
            "upload_speed_mbps",
            "upload_time",
            "upload_file_size",
            "latency",
            "test_state",
            "date",
        ]
        read_only_fields = ["id", "date"]
