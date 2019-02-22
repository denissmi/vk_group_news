from django.db import models


class VkPost(models.Model):
    text = models.TextField()
    picture = models.ImageField()
    publication_date = models.DateTimeField()
    message_id = models.IntegerField()
    link = models.URLField()

    class Meta:
        ordering = ('publication_date',)
