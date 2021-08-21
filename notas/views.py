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

    def get(self, request):
        form = CredentialsForm()
        return render(request, "register.html", {'form':form})

class HomeView(View):
    def get(self, request):
        notes  = Note.objects.filter(user=request.user).values('title', 'id').order_by('-modified_time')
        return render(request, 'home.html', {'notes':notes})

class NoteEditView(View):
    def post(self, request, note_id=None):
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['note']
            if note_id:
                try:
                    note = Note.objects.get(id=note_id, user=request.user)
                    print(note_id, note.id)
                except Note.DoesNotExist:
                    return HttpResponse(status=404)
                note.title = title
                note.note = content
            else:
                note = Note(title=title, note=content, user=request.user)
            note.save()
        return HttpResponseRedirect('/')

    def get(self, request, note_id=None):
        if note_id:
            try:
                note = Note.objects.get(id=note_id, user=request.user)
            except Note.DoesNotExist:
                return HttpResponse(status=404)
            form = NoteForm(initial={
                'title': note.title,
                'note': note.note,
            })
        else:
            form = NoteForm()

        return render(request, 'note_edit.html', {'form':form})

class NoteView(View):
    def get(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            return HttpResponse(status=404)
        note = {
            'title': note.title,
            'note': markdown(note.note),
        }
        return render(request, 'note.html', {'note':note})

class NoteDeleteview(View):
    def get(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            return HttpResponse(status=404)
        note.delete()
        return HttpResponseRedirect('/')
