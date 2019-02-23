from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from vk_group_news import views

urlpatterns = [
    path('vk_posts/', views.VkPostList.as_view()),
    path('vk_posts/<int:pk>', views.VkPostDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
