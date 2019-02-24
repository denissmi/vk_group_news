# Generated by Django 2.1.7 on 2019-02-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VkPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('image', models.ImageField(upload_to='vk_post_images')),
                ('publication_date', models.DateTimeField()),
                ('message_id', models.IntegerField()),
                ('link', models.URLField()),
            ],
            options={
                'ordering': ('publication_date',),
            },
        ),
    ]
