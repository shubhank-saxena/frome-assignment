# Generated by Django 5.0.4 on 2024-04-04 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TweetAuthor",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=256)),
                ("description", models.TextField()),
                ("followers", models.IntegerField()),
                ("following", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Tweet",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("tweet", models.CharField(max_length=256)),
                ("created_at", models.DateTimeField()),
                ("tweet_link", models.URLField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tweets.tweetauthor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TweetHashtag",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("hashtag", models.CharField(max_length=256)),
                (
                    "tweet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tweets.tweet"
                    ),
                ),
            ],
        ),
    ]
