from django.urls import path
from user.views import (
    Register,
    Login, 
    Profile, 
    Logout, 
    ReportedUsersView, 
    ReportedUserView, 
    ConnectionsView, 
    UserView,
    AddConnection,
    RemoveConnection
)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('connection/<pk>/add/', login_required(AddConnection.as_view()), name='add-connection'),
    path('connection/<pk>/delete/', login_required(RemoveConnection.as_view()), name='remove-connection'),
    path('login/', Login.as_view(), name='login'),
    path('profile/', login_required(Profile.as_view()), name='profile'),
    path('logout/', Logout, name='logout'),
    path('reported-users/', login_required(ReportedUsersView.as_view()),
         name='reported-users'),
    path('reported-users/<pk>/view/',
         login_required(ReportedUserView.as_view()), name='reported-user'),
    path('connections/', login_required(ConnectionsView.as_view()), name='connections'),
    path('user/<pk>/view/', login_required(UserView.as_view()), name='user'),
]
