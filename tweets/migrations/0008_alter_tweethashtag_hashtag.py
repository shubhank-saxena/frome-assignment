# Generated by Django 5.0.4 on 2024-04-04 19:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0007_remove_tweethashtag_tweet_alter_tweethashtag_hashtag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tweethashtag",
            name="hashtag",
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
    ]
