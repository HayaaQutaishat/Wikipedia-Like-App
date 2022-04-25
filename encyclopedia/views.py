from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
import random


class SearchForm(forms.Form):
    q = forms.CharField(label='')


class NewPageForm(forms.Form):
     entry_title = forms.CharField(label='Entry title', widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))
     content = forms.CharField(label='',widget=forms.Textarea(attrs={
      "placeholder": "Page Content",
      "class": "form-control col-md-8 col-lg-8",
      "rows": 10,
      }))


class EditForm(forms.Form):
     entry_title = forms.CharField(label='Entry title', widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))
     content = forms.CharField(label='',widget=forms.Textarea(attrs={
      "placeholder": "Page Content",
      "class": "form-control col-md-8 col-lg-8",
      "rows": 10,
      }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    md_entry = util.get_entry(title)
    if md_entry != None:
        HTML_entry = Markdown().convert(md_entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "HTML_entry": HTML_entry
        })
    else:
        return render(request, "encyclopedia/error.html",
        {
            "title": title
        })

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            md_entry = util.get_entry(q)
            if md_entry != None:
                return redirect(reverse('entry', args=[q]))
            else:
                list = []
                entries = util.list_entries()
                for entry in entries:
                    if q.upper() in entry.upper():
                        list.append(entry)

                return render(request, "encyclopedia/search.html", {
                    "list": list,
                    "q" : q,
                    "entries": util.list_entries()
                })

    return render(request, "encyclopedia/index.html", {
        "form" : SearchForm()
    })

def newpage(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            content = form.cleaned_data["content"]
            #if the title not exist
            if util.get_entry(entry_title) is None:
                util.save_entry(entry_title, content)
                return redirect(reverse('entry', args=[entry_title]))
            else:
                #if title already exist
                return render(request, "encyclopedia/exist.html",{
                    "entry_title": entry_title
                })

    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            content = form.cleaned_data["content"]
            util.save_entry(entry_title, content)
            return redirect(reverse('entry', args=[entry_title]))
        else:
            return render(request, "encyclopedia/edit.html",{
            "form": EditForm(),
            "entry_title": entry_title
        })

    return render(request, "encyclopedia/edit.html",{
        "form": EditForm()
    })

def randompage(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    if util.get_entry(entry) != None:
        HTML_entry = Markdown().convert(util.get_entry(entry))
        return render(request,"encyclopedia/random.html",{
            "random_page" : HTML_entry
        })










