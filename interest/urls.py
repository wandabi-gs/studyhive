from django.urls import path
from interest.views import (
    InterestsView, 
    InterestView, 
    MyInterestsView, 
    AddInterestsView, 
    DropInterestsView,
    RecommendationsView, 
    RecommendationView, 
    UserContentListView,
    UserContentView,
    ListUserContentView,
    VideoView,
    PostReview,
    AddCourseView,
    AddCourseContentView
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# add-course

urlpatterns = [
    path('user-content/course/recommendation/add/', login_required(AddCourseContentView.as_view()), name='add-course-recommendation'),
    path('user-content/course/add/', login_required(AddCourseView.as_view()), name='add-course'),
    path('user-content/', login_required(ListUserContentView.as_view()), name='user-content'),
    path('my-content/', login_required(UserContentListView.as_view()), name='my-content'),
    path('my-content/<pk>/', login_required(UserContentView.as_view()), name='my-content'),
    path('post-review/<pk>/', login_required(csrf_exempt(PostReview.as_view())), name='post-review'),
    path('<pk>/video/', login_required(VideoView.as_view()), name='recommendation-video'),
    path('<pk>/recommendation/', login_required(RecommendationView.as_view()), name='recommendation'),
    path('recommendations/', login_required(RecommendationsView.as_view()), name='recommendations'),
    path('<pk>/view/', InterestView.as_view(), name='interest'),
    path('<pk>/drop/', login_required(DropInterestsView.as_view()), name='drop-interest'),
    path('<pk>/add/', login_required(AddInterestsView.as_view()), name='add-interest'),
    path('user-view/', login_required(MyInterestsView.as_view()), name='my-interests'),
    path('view/', InterestsView.as_view(), name='interests'),
]