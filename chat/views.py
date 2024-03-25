from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from chat.models import UserGroup, GroupMember, GroupMessage
from django.contrib import messages
from user.views import contains_non_alpha

class GroupView(View):
    template_name = 'chat/group.html'
    
    def get(self, request, pk):
        context = {}
        try:
            membership = GroupMember.objects.filter(member=request.user).values_list("group__uid", flat=True)
            context['groups'] = UserGroup.objects.filter(uid__in=membership)
            context["group"] = UserGroup.objects.get(uid=pk)
            context["membership"] = GroupMember.objects.get(member=request.user, group=context["group"])
            context["members"] = GroupMember.objects.filter(Q(group=context["group"]),~Q(member=request.user))  
            context["chats"] = GroupMessage.objects.filter(group=context["group"]).order_by("date") 
            # messages.get_messages(request=request).used = True      
            
            return render(request, self.template_name, context)
            
        except GroupMember.DoesNotExist:
            return redirect('groups')
        
class JoinGroup(View):
    def get(self, request, pk):
        try:
            group = UserGroup.objects.get(uid=pk)
            try:
                GroupMember.objects.get(member=request.user, group=group)
                messages.add_message(request, messages.SUCCESS, "You are already a member of this group")
                return redirect('group', pk=pk)

            except GroupMember.DoesNotExist:
                if group.private:
                    GroupMember.objects.create(group=group, member=request.user, allowed=False)
                    messages.add_message(request, messages.SUCCESS, "Request to join group sent successfully")
                    return redirect('groups')
                
                else:
                    GroupMember.objects.create(group=group, member=request.user, role="member")
                    messages.add_message(request, messages.SUCCESS, "You have joined the group successfully")
                    return redirect('group', pk=pk)
        
        except:
            messages.add_message(request, messages.ERROR, "Failed to join group")
            return redirect('groups')


class GroupsView(View):
    template_name = 'chat/groups.html'
    
    def get(self, request):
        context = {}
        
        membership = GroupMember.objects.filter(member=request.user).values_list("group__uid", flat=True)
        context["groups"] = UserGroup.objects.filter(~Q(uid__in=membership))
        context["membership"] = UserGroup.objects.filter(uid__in=membership)
        print(context)
        
        return render(request, self.template_name, context)


    
class DeleteGroup(View):
    template_name = 'chat/delete.html'
    
    def get(self, request, pk):
        return render(request, self.template_name)
    
    def post(self, request, pk):
        return render(request, self.template_name)
    
    
class EditGroup(View):
    template_name = 'chat/edit.html'
    
    def get(self, request, pk):
        return render(request, self.template_name)
    
    def post(self, request, pk):
        return render(request, self.template_name)
    
    
class CreateGroup(View):
    template_name = 'chat/create.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        private = False
        if request.POST.get("private"):
            private = True
        try:
            UserGroup.objects.get(name__iexact=request.POST.get("name"))
            context = {"error": "A group with this name already exists"}
            return render(request, self.template_name, context)
        
        except UserGroup.DoesNotExist:
            if contains_non_alpha(request.POST.get('name')):
                context = {"error": "A group with this name already exists"}
                return render(request, self.template_name, context)                
                
            group = UserGroup.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                private=private
            )
            GroupMember.objects.create(group=group, member=request.user, role="admin")
            messages.add_message(request, messages.SUCCESS, f"Group '{group.name}' created successfully")
            return redirect('group', pk=group.uid)