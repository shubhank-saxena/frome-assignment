from django.urls import path

from tweets.views import HashtagListView, RetrievePostsView, HashtagAnalysisView

urlpatterns = [
    path('hashtags/', HashtagListView.as_view(), name='hashtags'),
    path('posts/', RetrievePostsView.as_view(), name='posts'),
    path('analysis/', HashtagAnalysisView.as_view(), name='analysis'),
]
