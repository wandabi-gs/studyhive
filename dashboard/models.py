from django.db import models
from user.models import CustomUser as User
from chat.models import UserGroup, GroupMember

class OnlineMember(models.Model):
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class SiteVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    visits = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)