from django.urls import path
from .views import TaskLIst, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', RegisterPage.as_view(), name="register" ),
    path("login/", CustomLoginView.as_view(), name= "login" ),
    path("logout/", LogoutView.as_view(next_page= 'login'), name='logout'),
    path("", TaskLIst.as_view(), name="tasks"),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("create-task/", TaskCreate.as_view(), name="task-create"),
    path("update/<int:pk>/", TaskUpdate.as_view(), name= "task-update"),
    path('delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    
    
]

