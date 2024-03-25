from django.urls import path
from django.contrib.auth.decorators import login_required
from chat.views import CreateGroup, EditGroup, DeleteGroup, GroupsView, GroupView, JoinGroup

urlpatterns = [
    path('group/<pk>/join/',login_required(JoinGroup.as_view()), name='join-group'),
    path('group/<pk>/view/',login_required(GroupView.as_view()), name='group'),
    path('groups/',login_required(GroupsView.as_view()), name='groups'),
    path('group/<pk>/delete/',login_required(DeleteGroup.as_view()), name='delete-group'),
    path('group/<pk>/edit/',login_required(EditGroup.as_view()), name='edit-group'),
    path('group/create/',login_required(CreateGroup.as_view()), name='create-group'),
]