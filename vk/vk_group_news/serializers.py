from rest_framework import serializers
from vk_group_news.models import VkPost


class VkPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VkPost
        fields = ('id', 'text', 'picture', 'publication_date', 'message_id', 'link')
