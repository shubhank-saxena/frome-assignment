# Generated by Django 5.0.4 on 2024-04-05 05:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0010_remove_tweet_hashtags"),
    ]

    operations = [
        migrations.AddField(
            model_name="tweet",
            name="hashtags",
            field=models.ManyToManyField(to="tweets.tweethashtag"),
        ),
    ]
