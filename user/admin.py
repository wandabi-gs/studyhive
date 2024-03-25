from django.contrib import admin
from user.models import CustomUser, Connection

class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "username", "is_active", "is_staff", "is_superuser"]
    list_editable = ["is_active"]
    search_fields = ["email", "username", "first_name", "last_name"]
    list_filter = ["is_active", "is_staff", "is_superuser"]

admin.site.register(CustomUser, UserAdmin)

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ["user", "connection", "created_at"]
    search_fields = ["user__email", "connection__email"]
    list_filter = ["created_at"]

admin.site.register(Connection, ConnectionAdmin)