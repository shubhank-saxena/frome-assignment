# Generated by Django 5.0.4 on 2024-04-04 18:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0006_tweethashtag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tweethashtag",
            name="tweet",
        ),
        migrations.AlterField(
            model_name="tweethashtag",
            name="hashtag",
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
