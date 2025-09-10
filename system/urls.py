from django.urls import path
from . import views

app_name='system'

urlpatterns = [
    path('login/', views.BlogLogin, name='login'),
    path('logout/', views.BlogLogout, name='logout'),
    path('register/', views.register, name='register'),

    path('send_email/', views.send_email, name='send_email'),


]