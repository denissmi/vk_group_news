from django.db import models
from drf_extra_fields.fields import Base64ImageField


class VkPost(models.Model):
    text = models.TextField(blank=True)
    image = Base64ImageField()
    publication_date = models.DateTimeField()
    message_id = models.IntegerField()
    link = models.URLField(null=True)

    class Meta:
        ordering = ('publication_date',)
