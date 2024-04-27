from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http.response import JsonResponse
from interest.models import (
    Category, 
    Interest, 
    Recommendation, 
    RecommendationNotes, 
    RecommendationVideo, 
    UserInterest, 
    UserContent, 
    UserContentRecommendation,
    UserReview, 
    RecommendationViews
)
from user.models import Connection

from engines.recommendation import get_interest_recommendations
from user.models import CustomUser as User
from studyhive.settings import hate_speech_detection

class ListUserContentView(View):
    template_name = 'user/content/manage-content.html'
    
    def get(self, request, pk):
        context = {}
        context["contents"] = UserContent.objects.filter(user=request.user, uid=pk)
        return render(request,self.template_name, context)
    
    def post(self, request, pk):
        return render(request,self.template_name)

class AddCourseContentView(View):
    template_name = 'user/content/add-recommendation.html'

    def get(self, request, pk):
        context = {}
        context["content"] = UserContent.objects.get(uid=pk)
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        userContent = UserContent.objects.get(uid=pk)

        content_type = request.POST.get('content_type')
        title = request.POST.get('title')
        description = request.POST.get('description')

        UserContentRecommendation.objects.create(
            user = request.user,
            content = userContent,
            title = title,
            description = description,
            content_type = content_type
        )

        messages.add_message(request, messages.SUCCESS, f"'{title}' has been added to your content collection")
        return redirect('my-content', pk=pk)

class AddCourseView(View):
    template_name = 'user/content/add-course.html'
    
    def get(self, request):
        context = {}
        interests, created = UserInterest.objects.get_or_create(user=request.user)
        context["interests"] = interests.interests.all()
        return render(request, self.template_name, context)
    
    def post(self, request):
        title = request.POST.get('name')
        interest = request.POST.get('interest')
        description = request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail')

        UserContent.objects.create(
            title=title,
            interest=Interest.objects.get(uid=interest),
            user=request.user,
            description=description,
            thumbnail=thumbnail
        )

        messages.add_message(request, messages.SUCCESS, f"'{title}' has been added to your content collection")
        return redirect('my-content')
    
class UserContentView(View):
    template_name = 'interest/content/view.html'

    def get(self, request, pk):
        context = {}
        context["content"] = UserContent.objects.get(uid=pk)
        context["recommendations"] = UserContentRecommendation.objects.filter(user_content=context["content"]).order_by('title')
        print(context["recommendations"])
        return render(request, self.template_name, context)
    
class UserContentListView(View):
    template_name = 'interest/content/list.html'
    
    def get(self, request):
        context = {}
        connections_user = Connection.objects.filter(user=request.user).values_list('connection__uid', flat=True)
        user_connections = Connection.objects.filter(connection=request.user).values_list('user__uid', flat=True)
        connections = list(connections_user) + list(user_connections)
        context["contents"] = UserContent.objects.filter(user__uid__in=connections)
        return render(request,self.template_name, context)
    
    def post(self, request):
        return render(request,self.template_name)
    
class DeleteCourseView(View):
    def get(self, request, pk):
        UserContent.objects.get(uid=pk).delete()
        messages.add_message(request, messages.SUCCESS, f"Course has been deleted")
        return redirect('my-content')

class MyContentView(View):
    template_name = 'user/content/manage-content.html'
    
    def get(self, request, pk):
        context = {}
        context["content"] = UserContent.objects.get(user=request.user, uid=pk)
        context["recommendations"] = UserContentRecommendation.objects.filter(user_content=context["content"]).order_by("title")
        return render(request,self.template_name, context)
    
    def post(self, request, pk):
        user_content = UserContent.objects.get(uid=pk)
        content = request.FILES.get('content')
        title = request.POST.get('title')
        description = request.POST.get('description')

        UserContentRecommendation.objects.create(
            user_content = user_content,
            content = content,
            title = title,
            description = description,
        )

        return redirect('my-content', pk=pk)

class MyContentListView(View):
    template_name = 'user/content/my-contents.html'
    
    def get(self, request):
        context = {}
        context["courses"] = UserContent.objects.filter(user=request.user)
        return render(request,self.template_name, context)
    
    def post(self, request):
        return render(request,self.template_name)
    
class PostReview(View):
    def post(self, request, pk):
        sentiment = request.POST.get('sentiment')
        review = request.POST.get('review')
        video = RecommendationVideo.objects.get(id=pk)
        userReview, created = UserReview.objects.get_or_create(user=request.user, recommendation=video)
        prediction = hate_speech_detection(review)
        if prediction:
            review = f"This review has been flagged as {prediction}"
            
        userReview.add_review(review)

        if sentiment:
            if sentiment == "like":
                userReview.user_like()

            else:
                userReview.user_dislike()
    
        userReview.save()
        return JsonResponse({"like" : userReview.like, "dislike" : userReview.dislike, "comment" : userReview.review})
    
    
class VideoView(View):
    template_name = 'interest/recommendation/video.html'
    
    def get(self, request, pk):
        context = {}
        context["video"] = RecommendationVideo.objects.get(uid=pk)    
        context["notes"], created = RecommendationNotes.objects.get_or_create(recommendation=context["video"], user=request.user)
        context["mreview"], created = UserReview.objects.get_or_create(recommendation=context["video"], user=request.user)
        context["reviews"] = UserReview.objects.filter( ~Q(user=request.user), recommendation=context["video"])

        return render(request, self.template_name, context)

    def post(self, request, pk):
        notes, created = RecommendationNotes.objects.get_or_create(recommendation__uid=pk, user=request.user)
        notes.notes = request.POST.get('notes')
        notes.save()
        return redirect('recommendation-video', pk=pk)

class RecommendationView(View):
    template_name = 'interest/recommendation/recommendation.html'
    
    def get(self, request, pk):
        context = {}
        context["recommendation"] = Recommendation.objects.get(uid=pk)
        context["videos"] = RecommendationVideo.objects.filter(recommendation=context["recommendation"])
        recommendationView, created = RecommendationViews.objects.get_or_create(recommendation=context["recommendation"], user=request.user)
        recommendationView.add_view()
        
        return render(request,self.template_name, context)
    
    def post(self, request, pk):
        return render(request,self.template_name)
    


class RecommendationsView(View):
    template_name = 'interest/recommendation/recommendations.html'
    
    def get(self, request):
        context = {}
        context["recommendations"] = get_interest_recommendations(request.user)

        if len(context["recommendations"]) == 0:            
            userInterest, created = UserInterest.objects.get_or_create(user=request.user)
            user_interest = userInterest.interests.all()

            user_interests = [u.uid for u in user_interest]
            
            context["recommendations"] = Recommendation.objects.filter(interest__uid__in=user_interests)

        interests = [recommendation.interest for recommendation in context["recommendations"]]
        context["interests"] = list(set(interests))
        
        return render(request,self.template_name, context)

    def post(self, request):
        return render(request,self.template_name)
    

class InterestView(View):
    template_name = 'interest/interest.html'
    
    def get(self, request, pk):
        context = {}
        context["interest"] = Interest.objects.get(uid=pk)        
        context["recommendations"] = Recommendation.objects.filter(interest=context["interest"])    

        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        return render(request,self.template_name)
    

class MyInterestsView(View):
    template_name = 'interest/user/interests.html'
    
    def get(self, request):
        context = {}
        userInterest, created = UserInterest.objects.get_or_create(user=request.user)
        context["interests"] =  userInterest.interests.all()
        categories = set()

        for interest in context["interests"]:
            categories.add(interest.category)

        context["categories"] = list(categories)
        return render(request, self.template_name, context)
    
    def post(self, request):
        return render(request,self.template_name)
    


class DropInterestsView(View):    
    def get(self, request, pk):     
        try:   
            interest = Interest.objects.get(uid=pk)
            userInterest, created = UserInterest.objects.get_or_create(user=request.user)
            userInterest.interests.remove(interest)
            messages.add_message(request, messages.SUCCESS, f"'{interest.name}' has been droped from your interest collection")
        
        except:
            pass

        try:
            referring_url = request.META.get('HTTP_REFERER')
            
            if referring_url:
                return redirect(referring_url)
            
        except:
            pass
        
        return redirect('my-interests')
    

class AddInterestsView(View):    
    def get(self, request, pk):        
        interest = Interest.objects.get(uid=pk)
        userInterest, created = UserInterest.objects.get_or_create(user=request.user)
        userInterest.interests.add(interest)
        messages.add_message(request, messages.SUCCESS, f"'{interest.name}' has been added to your interest collection")
        
        try:
            referring_url = request.META.get('HTTP_REFERER')
            
            if referring_url:
                return redirect(referring_url)
            
        except:
            pass
        
        return redirect('my-interests')


class InterestsView(View):
    template_name = 'interest/interests.html'
    
    def get(self, request):
        context = {}
        context["categories"] = Category.objects.all()
        context["interests"] = Interest.objects.all()  
        context["minterests"] = None

        if request.user.is_authenticated:
            interests, created = UserInterest.objects.get_or_create(user=request.user)
            context["minterests"] = interests.interests.all()      

        return render(request, self.template_name, context)