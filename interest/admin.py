from django.contrib import admin
from interest.models import UserReview, UserInterest, UserContent, Category, Interest

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name", "description", "created_at"]
    search_fields = ["name"]

admin.site.register(Category, CategoryAdmin)


class InterestAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "description", "created_at"]
    search_fields = ["name","category__name"]

admin.site.register(Interest, InterestAdmin)

class UserReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "recommendation", "like", "dislike", "updated_at"]
    search_fields = ["user__email", "recommendation__title"]
    list_filter = ["updated_at"]

admin.site.register(UserReview, UserReviewAdmin)

class UserInterestAdmin(admin.ModelAdmin):
    list_display = ["user","selected_interests", "created_at"]
    search_fields = ["user__email"]
    list_filter = ["created_at"]

    def selected_interests(self, obj):
        interests = obj.interests.all()[:5]
        return ", ".join([interest.name for interest in interests.all()])

admin.site.register(UserInterest, UserInterestAdmin)


class UserContentAdmin(admin.ModelAdmin):
    list_display = ["user", "interest", "title"]
    search_fields = ["user__email", "interest__name"]
    list_filter = ["interest"]

admin.site.register(UserContent, UserContentAdmin)
# Register your models here.
