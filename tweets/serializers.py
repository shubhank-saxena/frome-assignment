from rest_framework import serializers
from tweets.models import Tweet, TweetAuthor, TweetHashtag

class TweetHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetHashtag
        fields = '__all__'

class TweetAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetAuthor
        fields = ['username']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['username']

class TweetSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='hashtag'
    )
    author = serializers.StringRelatedField()

    class Meta:
        model = Tweet
        fields = ['tweet', 'created_at', 'tweet_link', 'author', 'hashtags']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {instance.id: representation}
