from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path('login/', views.login_view.as_view(), name='login'),
  path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
  path('register/', views.register.as_view(), name='register'),

  path('', views.task_list.as_view(), name='task-list'),
  path('task/<int:pk>/', views.task.as_view(), name='task'),
  path('task-create/', views.task_create.as_view(), name='task-create'),
  path('task-update/<int:pk>', views.task_update.as_view(), name="task-update"),
  path('task-delete/<int:pk>', views.task_delete.as_view(), name="task-delete"),
]