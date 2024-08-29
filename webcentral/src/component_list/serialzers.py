from rest_framework import serializers
from .models import (
    Component,
)  # Replace with the actual path to your Component model


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = "__all__"
