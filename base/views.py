from django.shortcuts import redirect, render
# from django.http import HttpResponse no need for httpresponse when using class-based view
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from base.models import Task
from django.urls import reverse_lazy

# Create your views here.
#note: class-based views look for specific htmls

class CustomLoginView(LoginView):  
    model=Task
    template_name: str= 'base/login.html'
    fields= "__all__"
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name= 'base/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user=True
    success_url= reverse_lazy('tasks')

    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

        
class TaskLIst(LoginRequiredMixin,ListView):
    #list view looks for object_list
    model= Task
    context_object_name= "tasks" #by default this is "object_list"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(complete= False).count()
        search_input= self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']= context['tasks'].filter(title__icontains=search_input) #you can add a startswith to find items that begin with the particular letter passed in
        
        context['search-input']= search_input
        return context



class TaskDetail(LoginRequiredMixin, DetailView):
    #detailview looks for object
    model= Task
    context_object_name: str=  'task' #by default this is object
    template_name: str= "base/task.html" #by default list view finds a html template with named after the class it's assigned to. this function "template_name" is to change such


class TaskCreate(LoginRequiredMixin, CreateView): 
    model= Task
    template_name: str='base/task_form.html'
    fields= ['title', 'description', 'complete']
    success_url= reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate, self).form_valid(form)



class TaskUpdate(LoginRequiredMixin, UpdateView):
    model= Task
    fields= ['title', 'description', 'complete']
    success_url= reverse_lazy("tasks")

class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    context_object_name: str= "task"
    success_url= reverse_lazy("tasks")
    

