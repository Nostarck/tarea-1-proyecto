from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django import forms
from django.contrib.auth.models import User
from markdown import markdown

from notas.models import  *

class CredentialsForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class NoteForm(forms.Form):
    title = forms.CharField(label='Note title', max_length=100)
    note = forms.CharField(label='Note content', widget=forms.Textarea)
    
class RegisterView(View):
    def post(self, request):
        form = CredentialsForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            return HttpResponseRedirect('/')
