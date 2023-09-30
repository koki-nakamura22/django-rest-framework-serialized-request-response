from rest_framework import serializers


class TestGetRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, required=True)


class TestGetResponseSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False, required=True)
    age = serializers.IntegerField(allow_null=False, required=True)


class TestPostRequestSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False, required=True)
    age = serializers.IntegerField(allow_null=False, required=True)


class TestPostResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, required=True)
