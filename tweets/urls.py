from django.urls import path

from tweets.views import HashtagAnalysisView, HashtagListView, RetrievePostsView

urlpatterns = [
    path("hashtags/", HashtagListView.as_view(), name="hashtags"),
    path("posts/", RetrievePostsView.as_view(), name="posts"),
    path("analysis/", HashtagAnalysisView.as_view(), name="analysis"),
]
