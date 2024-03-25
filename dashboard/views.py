from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q, F, Aggregate, Avg, Count, Sum, Subquery, OuterRef
import random
from user.models import CustomUser as User
from datetime import datetime, timedelta

from interest.models import (
    Category,
    Interest,
    Recommendation,
    RecommendationViews,
    RecommendationVideo,
    UserReview
)

from chat.models import UserGroup

from django.http import HttpResponse
from django_xhtml2pdf.utils import generate_pdf

class DeleteInterest(View):
    def get(self, request, pk):
        interest = Interest.objects.get(uid=pk)
        interest.delete()
        return redirect('dashboard-interests')

class InterestView(View):
    template_name = 'dashboard/interest/interest.html'

    def get(self, request, pk):
        context = {}
        context["interest"] = Interest.objects.get(uid=pk)
        context["categories"] = Category.objects.all()
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = Category.objects.get(uid = request.POST.get('category'))
        interest = Interest.objects.get(uid=pk)
        interest.name = name
        interest.description = description
        interest.category = category
        interest.save()
        return redirect('dashboard-interest', pk=pk)
    

class InterestsView(View):
    template_name = 'dashboard/interest/interests.html'

    def get(self, request):
        context = {}
        context["interests"] = Interest.objects.all()
        return render(request, self.template_name, context)
    
class CategoryView(View):
    template_name = 'dashboard/category/category.html'

    def get(self, request, pk):
        context = {}
        context["category"] = Category.objects.get(uid=pk)
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = Category.objects.get(uid=pk)
        category.name = name
        category.description = description
        category.save()
        return redirect('dashboard-category', pk=pk)
    

class CategoriesView(View):
    template_name = 'dashboard/category/categories.html'

    def get(self, request):
        context = {}
        context["categories"] = Interest.objects.values('category').annotate(total=Count('category')).order_by('-total')
        return render(request, self.template_name, context)
    

class UserView(View):
    template_name = 'dashboard/user/user.html'

    def get(self, request, pk):
        context = {}
        context["duser"] = User.objects.get(id=pk)
        context["interests"] = Interest.objects.filter(userinterest__user=context["duser"])
        context["groups"] = UserGroup.objects.filter(users=context["user"])
        context["recommendations"] = Recommendation.objects.filter(Q(user=context["duser"]) | Q(group__users=context["duser"])).distinct()
        return render(request, self.template_name, context)


class UsersView(View):
    template_name = 'dashboard/user/users.html'

    def get(self, request):
        context = {}
        context["users"] = User.objects.all()
        return render(request, self.template_name, context)


class Home(View):
    template_name = 'dashboard/home.html'

    def get(self, request):
        context = {}

        context["users"] = User.objects.count()
        context["groups"] = UserGroup.objects.count()
        context["interests"] = Interest.objects.count()
        context["recommendations"] = Recommendation.objects.count()

        interest_views = Interest.objects.annotate(total_views=Sum('recommendation__recommendationviews__views'))

        top_interests = list(interest_views.order_by('-total_views'))[:5]
        random.shuffle(top_interests)
            
        context["title_recommendation_views"] = [interest.name for interest in top_interests]
        context["values_recommendation_views"] = [interest.total_views if interest.total_views else 0 for interest in top_interests]

        top_liked_interests = list(Interest.objects.filter(recommendation__recommendation_videos__userreview__like=True).values('id', 'name').annotate(like_count=Count('recommendation__recommendation_videos__userreview')).order_by('-like_count'))[:5]
        
        random.shuffle(top_liked_interests)
        context["liked_title"] = [interest["name"] for interest in top_liked_interests]
        context["liked_values"] = [interest["like_count"] for interest in top_liked_interests]

        top_disliked_interests = list(Interest.objects.filter(recommendation__recommendation_videos__userreview__dislike=True).values('id', 'name').annotate(dislike_count=Count('recommendation__recommendation_videos__userreview')).order_by('-dislike_count'))[:5]
        
        random.shuffle(top_disliked_interests)
        context["disliked_title"] = [interest["name"] for interest in top_disliked_interests]
        context["disliked_values"] = [interest["dislike_count"] for interest in top_disliked_interests]

        return render(request, self.template_name, context)
    
    def post(self, request):
        context = {}
        from_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")

        try:
            if request.POST.get('from_date'):
                from_date = datetime.strptime(request.POST.get('from_date'), "%Y-%m-%d")            

        except:
            from_date = datetime.strptime("2024-01-01", "%Y-%m-%d")

        try:
            if request.POST.get('to_date'):
                to_date = datetime.strptime(request.POST.get('to_date'), "%Y-%m-%d")

        except:
            to_date = datetime.now().strftime("%Y-%m-%d")
            to_date = datetime.strptime(to_date, "%Y-%m-%d")

        to_date_real = to_date
        to_date += timedelta(days=1)
        from_date = from_date.date()
        to_date = to_date.date()

        filtered_recommendation_views = RecommendationViews.objects.filter(
            recommendation_id=OuterRef('pk'),
            date__range=[from_date, to_date]
        )

        recommendations_with_views = Recommendation.objects.annotate(
            total_views=Sum('recommendationviews__views')
        ).filter(
            pk__in=Subquery(filtered_recommendation_views.values('recommendation_id'))
        ).order_by('-total_views')[:10]

        context["from_date"] = from_date
        context["to_date"] = to_date_real.date()
        context["print_date"] = datetime.now()

        context["top_interests"] = recommendations_with_views
        context["top_disliked_interests"] = Recommendation.objects.filter(recommendation_videos__userreview__dislike=True, recommendation_videos__userreview__updated_at__range=[from_date, to_date]).annotate(dislike_count=Count('recommendation_videos__userreview')).order_by('-dislike_count')[:10]
        context["top_liked_interests"] = Recommendation.objects.filter(recommendation_videos__userreview__like=True, recommendation_videos__userreview__updated_at__range=[from_date, to_date]).annotate(like_count=Count('recommendation_videos__userreview')).order_by('-like_count')[:10]
        
        context["most_selected_interest"] = Interest.objects.annotate(user_selection=Count('userinterest'), group_selection=Count('group_interests')).order_by('-user_selection')[:10]

        template_name = 'dashboard/report.html'
        response = HttpResponse(content_type='application/pdf')

        result = generate_pdf(template_name=template_name, context=context, file_object=response)
        return result

# from random import randint

# rs = RecommendationVideo.objects.all()
# users = User.objects.all()
# def execute():
#     x = randint(0, len(rs)-1)
#     y = randint(0, len(users)-1)
#     z = randint(0, 1)

#     review = UserReview(user=users[y], recommendation=rs[x])
#     if z==0:
#         review.like=True

#     else:
#         review.dislike = True

#     review.save()


