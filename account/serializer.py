from rest_framework import serializers
from .models import Certifications


class CertificationsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certifications
        fields = ["certificate_name"]
