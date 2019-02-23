from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from vk_group_news.models import VkPost
from vk_group_news.serializers import VkPostSerializer


class VkPostList(APIView):
    """List all vk posts or create a new post"""
    def get(self, request, format=None):
        vk_posts = VkPost.objects.all()
        serializer = VkPostSerializer(vk_posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VkPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VkPostDetail(APIView):
    """Retrieve, update or delete a vk port"""
    def get_object(self, pk):
        try:
            vk_post = VkPost.objects.get(pk=pk)
        except VkPost.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vk_post = self.get_object(pk)
        serializer = VkPostSerializer(vk_post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vk_post = self.get_object(pk)
        serializer = VkPostSerializer(vk_post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vk_post = self.get_object(pk)
        vk_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
