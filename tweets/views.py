from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
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

    @swagger_auto_schema(
        operation_description="Get a list of all hashtags.",
        responses={
            200: openapi.Response(
                description="List of all hashtags.",
                schema=TweetHashtagSerializer(many=True),
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RetrievePostsView(generics.ListAPIView):
    """Search posts view."""

    serializer_class = TweetSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_description="Get a list of tweets based on a keyword.",
        manual_parameters=[
            openapi.Parameter(
                name="keyword",
                in_=openapi.IN_QUERY,
                description="Keyword to search for in tweets and hashtags.",
                type=openapi.TYPE_STRING,
                required=True,
                example="black",
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of tweets that match the keyword.",
                schema=TweetSerializer(many=True),
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request - no keyword provided",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
        return Response(
            {"error": "No keyword provided"}, status=status.HTTP_400_BAD_REQUEST
        )


class HashtagAnalysisView(APIView):
    """Hashtag analysis view."""

    @swagger_auto_schema(
        operation_description="Get analysis of tweets for a specific hashtag.",
        manual_parameters=[
            openapi.Parameter(
                name="hashtag",
                in_=openapi.IN_QUERY,
                description="Hashtag to analyze.",
                type=openapi.TYPE_STRING,
                required=True,
                example="facebook",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Analysis of tweets that include the hashtag.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "tweets_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "authors_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "authors_list": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                        ),
                        "first_tweet_date": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date-time"
                        ),
                        "last_tweet_date": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date-time"
                        ),
                        "sentiment_of_tweets": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "positive": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "negative": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "neutral": openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                        ),
                    },
                ),
            ),
            400: "Bad request - no hashtag provided.",
        },
    )
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
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "No hashtag provided"}, status=status.HTTP_400_BAD_REQUEST
        )
