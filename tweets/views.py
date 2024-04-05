from django.db.models import Q
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from textblob import TextBlob

from tweets.models import Tweet, TweetHashtag
from tweets.serializers import TweetHashtagSerializer, TweetSerializer


def sentiment_analysis(text):
    """Perform sentiment analysis on text."""
    blob = TextBlob(text)
    return blob.sentiment.polarity


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination settings."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000


class HashtagListView(generics.ListAPIView):
    """Hashtag list view."""

    queryset = TweetHashtag.objects.all()
    serializer_class = TweetHashtagSerializer
    pagination_class = StandardResultsSetPagination


class RetrievePostsView(generics.ListAPIView):
    """Search posts view."""

    serializer_class = TweetSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        keyword = self.request.query_params.get("keyword", None)
        if keyword is not None:
            return (
                Tweet.objects.select_related("author")
                .prefetch_related("hashtags")
                .filter(
                    Q(tweet__icontains=keyword)
                    | Q(hashtags__hashtag__icontains=keyword)
                )
                .distinct()
            )
        return Tweet.objects.none()


class HashtagAnalysisView(APIView):
    """Hashtag analysis view."""

    def get(self, request, *args, **kwargs):
        hashtag = request.query_params.get("hashtag", None)
        if hashtag is not None:
            tweet_objects = (
                Tweet.objects.filter(hashtags__hashtag__iexact=hashtag)
                .order_by("created_at")
                .select_related("author")
                .prefetch_related("hashtags")
            )
            count = tweet_objects.count()
            sentiment_of_tweets = {"positive": 0, "negative": 0, "neutral": 0}
            authors = set()
            for tweet in tweet_objects:
                tweet_sentiment = sentiment_analysis(tweet.tweet)
                if 0.2 < tweet_sentiment <= 1.0:
                    sentiment_of_tweets["positive"] += 1
                elif -0.2 < tweet_sentiment <= 0.2:
                    sentiment_of_tweets["neutral"] += 1
                else:
                    sentiment_of_tweets["negative"] += 1
                authors.add(tweet.author.username)

            return Response(
                {
                    "tweets_count": count,
                    "authors_count": len(authors),
                    "authors_list": list(authors),
                    "first_tweet_date": tweet_objects.first().created_at,
                    "last_tweet_date": tweet_objects.last().created_at,
                    "sentiment_of_tweets": sentiment_of_tweets,
                }
            )
        return Response({"error": "No hashtag provided"}, status=400)
