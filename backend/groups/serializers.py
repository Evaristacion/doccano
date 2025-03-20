from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

class PermissionSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = "__all__"

    def get_description(self, obj):
        return f"{obj.content_type.app_label} | {obj.content_type.model} | {obj.name}"
    


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    permission_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Group
        fields = "__all__"

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        group = super().create(validated_data)
        group.permissions.set(permission_ids)
        return group

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        group = super().update(instance, validated_data)
        group.permissions.set(permission_ids)
        return group