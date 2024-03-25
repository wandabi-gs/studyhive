from django.contrib import admin
from chat.models import UserGroup, GroupMember

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ["uid","name", "description", "created_at"]
    search_fields = ["name", "admin__email"]
    list_filter = ["created_at"]

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ["group", "member", "role", "created_at"]
    search_fields = ["group__name", "member__email"]
    list_filter = ["created_at"]
