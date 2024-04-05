from django.contrib import admin

from tweets.models import Tweet, TweetAuthor, TweetHashtag

# Register your models here.

admin.site.register(Tweet)
admin.site.register(TweetAuthor)
admin.site.register(TweetHashtag)
