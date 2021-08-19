"""notas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from notas.views import *

urlpatterns = [
    path('', login_required(HomeView.as_view(), login_url='login'), name='home'),
    path('login', LoginView.as_view(redirect_authenticated_user=True, template_name='login.html'), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('new_note', login_required(NoteEditView.as_view(), login_url='login'), name='new_note'),
    path('note/<int:note_id>', login_required(NoteView.as_view(), login_url='login'), name='note'),
    path('note/<int:note_id>/edit', login_required(NoteEditView.as_view(), login_url='login'), name='note_edit'),
    path('note/<int:note_id>/delete', login_required(NoteDeleteview.as_view(), login_url='login'), name='note_delete'),
]
