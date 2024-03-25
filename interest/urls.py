from django.urls import path
from interest.views import (
    InterestsView, 
    InterestView, 
    MyInterestsView, 
    AddInterestsView, 
    DropInterestsView,
    RecommendationsView, 
    RecommendationView, 
    UserContentView,
    VideoView
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('user-content/', login_required(UserContentView.as_view()), name='user-content'),
    path('<pk>/video/', login_required(VideoView.as_view()), name='recommendation-video'),
    path('<pk>/recommendation/', login_required(RecommendationView.as_view()), name='recommendation'),
    path('recommendations/', login_required(RecommendationsView.as_view()), name='recommendations'),
    path('<pk>/view/', InterestView.as_view(), name='interest'),
    path('<pk>/drop/', login_required(DropInterestsView.as_view()), name='drop-interest'),
    path('<pk>/add/', login_required(AddInterestsView.as_view()), name='add-interest'),
    path('user-view/', login_required(MyInterestsView.as_view()), name='my-interests'),
    path('view/', InterestsView.as_view(), name='interests'),
]