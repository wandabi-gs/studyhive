from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    Home,
    UserView,
    UsersView,
    CategoriesView,
    CategoryView,
    InterestsView,
    InterestView,
    DeleteInterest
)

urlpatterns = [
    path('', login_required(Home.as_view()), name='dashboard'),
    path('user/<user_id>/', login_required(UserView.as_view()),
         name='dashboard-user'),
    path('users/', login_required(UsersView.as_view()), name='dashboard-users'),
    path('categories/', login_required(CategoriesView.as_view()),
         name='dashboard-categories'),
    path('category/<pk>/', login_required(CategoryView.as_view()),
         name='dashboard-category'),
    path('interests/', login_required(InterestsView.as_view()),
         name='dashboard-interests'),
    path('interest/<pk>/', login_required(InterestView.as_view()),
         name='dashboard-interest'),
    path('interest/delete/<pk>/', login_required(DeleteInterest.as_view()), name='delete-interest'),
]
