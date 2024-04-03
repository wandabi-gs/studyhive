from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import re
from django.db.models import Q
from user.models import (
    CustomUser as User,
    Connection,
    ReportedUser
)
from engines.user import get_user_recommendations
from datetime import datetime
from dashboard.models import SiteVisit

def contains_non_alpha(name):
    return bool(re.search(r'[^a-zA-Z\s]', name))

def email_valid(email):
    regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return regex.match(email)    
    

class ReportedUserView(View):
    template_name = 'user/reportedusers.html'
    
    def get(self, request, pk):
        
        return render(request, self.template_name)
    
    def post(self, request, pk):
        return render(request, self.template_name)
    

class ReportedUsersView(View):
    template_name = 'user/reportedusers.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        return render(request, self.template_name)


class UserView(View):
    template_name = 'user/user.html'
    
    def get(self, request, pk):
        return render(request, self.template_name)
    
    def post(self, request, pk):
        return render(request, self.template_name)
    
    
class RemoveConnection(View):
    def get(self, request, pk):
        connection = User.objects.get(uid=pk)
        
        try:
            con = Connection.objects.get(Q(connection=connection) | Q(user=connection))   
            con.delete()
            
            messages.add_message(request, messages.SUCCESS, f"User '{connection.username}' has been removed from your connections")

        except Connection.DoesNotExist:
            pass

        return redirect('connections')      
    

class AddConnection(View):
    def get(self, request, pk):
        connection = User.objects.get(uid=pk)
        try:
            Connection.objects.get(Q(connection=connection) | Q(user=connection))   

        except Connection.DoesNotExist:
            Connection.objects.create(user=request.user, connection=connection)
            messages.add_message(request, messages.SUCCESS, f"User '{connection.username}' has been added to your connections")

        return redirect('connections')      

class ConnectionsView(View):
    template_name = 'user/connections.html'
    
    def get(self, request):
        connections = Connection.objects.filter(Q(user=request.user) | Q(connection=request.user))
        recommendations = get_user_recommendations(request.user)
        
        context = {
            "connections" : connections,
            "recommendations" : recommendations
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        return render(request, self.template_name)

def Logout(request):
    
    logout(request=request)
    return redirect('home')


class Profile(View):
    template_name = 'user/profile.html'

    def get(self, request):
        return render(request=request, template_name=self.template_name)
    
    def post(self, request):
        context = {}
        if "type" in request.POST:
            if request.POST.get('type') == "profile":

                if not email_valid(request.POST.get('email')):
                    context["profile_error"] = "Please enter a valid email"
                    return render(request, self.template_name, context)
                
                if not "image" in request.FILES and (request.POST.get('email') == request.user.email):
                    return render(request, self.template_name, context)
                
                user = request.user
                if "image" in request.FILES:
                    user.image = request.FILES["image"]

                try:
                    User.objects.get(email=request.POST.get('email'))
                    user.save()
                    context["profile_error"] = "This email is already registered to another user"
                    
                except User.DoesNotExist:
                    if not request.POST.get('email') == request.user.email:
                        user.email = request.POST.get('email')

                    user.save()
                    messages.add_message(request, messages.SUCCESS, "Profile updated successfully")
                    return redirect('profile')
                        
            if request.POST.get('type') == "password":
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                context = {
                    'old_password' : old_password,
                    'new_password' : new_password,
                    'confirm_password' : confirm_password
                }
                
                if len(new_password) < 8:
                    context["password_error"] = "Password must have atleast 8 characters"
                    return render(request, self.template_name, context)
                
                if not request.user.check_password(old_password):
                    context["password_error"] = "Old password is incorrect"
                    return render(request, self.template_name, context)
                
                if new_password != confirm_password:
                    context["password_error"] = "Passwords do not match"
                    return render(request, self.template_name, context)   
                
                user = request.user
                user.set_password(new_password)
                user.save()         
                messages.add_message(request, messages.SUCCESS, "Password updated successfully")
                logout(request)
                return redirect('login')
                    
        return render(request=request, template_name=self.template_name, context=context)


class Login(View):
    template_name = 'user/login.html'

    def get(self, request):
        return render(request=request, template_name=self.template_name)
    
    def post(self, request):
        next = None
        if "next" in request.GET:
            next = request.GET["next"]
            
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            "email" : email,
            "password" : password,
            "error" : None
        }
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request=request, user=user)
                messages.add_message(request, messages.SUCCESS, "User login was succesful")

                visit, created = SiteVisit.objects.get_or_create(user=user, date=datetime.now().date())
                if not created:
                    visit.visits += 1
                    visit.save()
                
                print(visit, created)

                if user.is_staff:
                    return redirect('dashboard')
                
                if next:
                    return redirect(next)
                
                return redirect('home')
            
            else:
                context["error"] = "Invalid login details provided"

        except User.DoesNotExist:
            context["error"] = "Invalid login details provided"


        return render(request=request, template_name=self.template_name, context=context)
    

class Register(View):
    template_name = 'user/register.html'

    def get(self, request):
        return render(request=request, template_name=self.template_name)
    
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {
            "email" : email,
            "password" : password,
            "username" : username,
            "error" : None
        }
        if not password or not username or not email:
            context["error"] = "please fill out all fields"
            
        if contains_non_alpha(username):
            context["error"] = "Please enter a valid name"
            return render(request=request, template_name=self.template_name, context=context)

        else:
            try:
                User.objects.get(email=email)
                context["error"] = "Another account is registered to this email"

            except User.DoesNotExist:
                if len(password) < 8:
                    context["error"] = "Password must have atleast 8 characters"

                else:
                    try:
                        user = User(email=email, username=str(username).upper())
                        user.set_password(password)
                        user.save()
                        messages.add_message(request, messages.SUCCESS, "Account created succesully")
                        return redirect("login")

                    except Exception as e:
                        context["error"] = str(e)
        
        return render(request=request, template_name=self.template_name, context=context)