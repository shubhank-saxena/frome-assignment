from django.db import models

# Create your models here.

class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tweet = models.TextField()
    created_at = models.DateTimeField()
    tweet_link = models.URLField()
    author = models.ForeignKey('TweetAuthor', on_delete=models.CASCADE)
    hashtags = models.ManyToManyField('TweetHashtag')

    def __str__(self):
        return self.tweet

class TweetAuthor(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=256)
    followers = models.IntegerField()
    following = models.IntegerField()

    def __str__(self):
        return self.username

class TweetHashtag(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    hashtag = models.CharField(max_length=256, unique=True, null=True)

    def __str__(self):
        return self.tweet
