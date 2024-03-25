from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from interest.models import Interest

User = get_user_model()

class UserGroup(models.Model):
    uid = models.UUIDField(default=uuid4, unique=True)
    name = models.CharField(max_length=50)
    private = models.BooleanField(default=False)
    on_call = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True)
    interests = models.ManyToManyField(Interest, related_name="group_interests")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def latest(self):
        gmessage = GroupMessage.objects.filter(group=self).order_by('-date').first()

        username = gmessage.member.member.username if gmessage else ""
        message = gmessage.message if gmessage else "No message yet"
        data = {
            "username" : username,
            "message" : message
        }

        return data
    
    class Meta:
        verbose_name = "User Group"
        verbose_name_plural = "User Groups"
        ordering = ["name"]

roles = [
    ('admin', 'admin'),
    ('member', 'member')
]

class GroupMember(models.Model):
    uid = models.UUIDField(default=uuid4, unique=True)
    group = models.ForeignKey(UserGroup,on_delete=models.CASCADE)
    member = models.ForeignKey(User,related_name="group_member",on_delete=models.CASCADE)
    online = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=roles, default='member')
    allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.group.name} - {self.member.email}"
    class Meta:
        verbose_name = "Group Member"
        verbose_name_plural = "Group Members"
        ordering = ["-created_at"]

class GroupMessage(models.Model):
    group = models.ForeignKey(UserGroup,on_delete=models.CASCADE)
    member = models.ForeignKey(GroupMember,related_name="group_message_member",on_delete=models.CASCADE)
    message = models.TextField()
    upload = models.FileField(upload_to='chat/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class GroupVoiceCall(models.Model):
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
    participants = models.ManyToManyField(GroupMember, related_name="voice_call_participants")
    is_active = models.BooleanField(default=False)