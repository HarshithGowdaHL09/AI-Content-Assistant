from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='ai_assistant_index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.get_content, name='get_content'),
]

