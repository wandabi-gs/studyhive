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
    UserReview, 
    RecommendationViews
)

from engines.recommendation import get_interest_recommendations
from user.models import CustomUser as User


class UserContentView(View):
    template_name = 'interest/interests.html'
    
    def get(self, request):
        return render(request,self.template_name)
    
    def post(self, request):
        return render(request,self.template_name)
    
class PostReview(View):
    def post(self, request, pk):
        sentiment = request.POST.get('sentiment')
        review = request.POST.get('review')
        video = RecommendationVideo.objects.get(id=pk)
        userReview, created = UserReview.objects.get_or_create(user=request.user, recommendation=video)
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