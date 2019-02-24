from django.db import models


class VkPost(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='vk_post_images')
    publication_date = models.DateTimeField()
    message_id = models.IntegerField()
    link = models.URLField()

    class Meta:
        ordering = ('publication_date',)
