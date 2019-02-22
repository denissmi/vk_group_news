from rest_framework import serializers
from vk_group_news.models import VkPost


class VkPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    picture = serializers.ImageField()
    publication_date = serializers.DateTimeField()
    message_id = serializers.IntegerField()
    link = serializers.URLField()

    def create(self, validated_data):
        return VkPost.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.message_id = validated_data.get('message_id', instance.message_id)
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance
