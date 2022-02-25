from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task

# Create your views here.


class login_view(LoginView):
  fields = '__all__'
  template_name='base/login.html'
  redirect_authenticated_user = True

  def get_success_url(self):
    return reverse_lazy('task-list')




class register(FormView):
  template_name='base/register.html'
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url = reverse_lazy('task-list')

  def form_valid(self, form):
    user = form.save()
    if user is not None:
      login(self.request, user)
      return super(register, self).form_valid(form)

  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('task-list')
    return super(register,self).get(*args, **kwargs)


class task_list(LoginRequiredMixin, ListView):
  model = Task
  context_object_name = 'tasks'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['tasks'] = context['tasks'].filter(user=self.request.user)
      context['count'] = context['tasks'].count()
      context['incompleted_tasks'] = context['tasks'].filter(completed=False).count()
      context['completed_tasks'] = context['count'] - context['incompleted_tasks']

      search_keyword = self.request.GET.get('search-keyword') or ''
      if search_keyword:
        context['search_keyword'] = search_keyword
        context['tasks'] = context['tasks'].filter(title__icontains = search_keyword)
      return context 


class task(LoginRequiredMixin, DetailView):
  model = Task
  context_object_name = 'task'




class task_create(LoginRequiredMixin, CreateView):
  model = Task
  context_object_name = 'task'
  fields = ['title', 'description', 'completed']
  success_url = reverse_lazy('task-list')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(task_create, self).form_valid(form)



class task_update(LoginRequiredMixin, UpdateView):
  model = Task
  context_object_name = 'task'
  fields = ['title', 'description', 'completed']
  success_url = reverse_lazy('task-list')



class task_delete(LoginRequiredMixin, DeleteView):
  model = Task
  context_object_name = 'task'
  fields = '__all__'
  success_url = reverse_lazy('task-list')
















