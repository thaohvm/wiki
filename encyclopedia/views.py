from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from markdown2 import markdown
from random import choice

from . import util


class NewForm(forms.Form):
    class TitleField(forms.CharField):
        def validate(self, value):
            super().validate(value)
            if value in util.list_entries():
                raise ValidationError(f"ERROR: Title {value} already exists!")

    title = TitleField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea())


class EditForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, page):
    if page in util.list_entries():
        return render(request, "encyclopedia/page.html", {
            "page": page,
            "content": markdown(util.get_entry(page)),
            "entries": util.list_entries()
        })
    else:
        return HttpResponseNotFound("Page not found")


def search(request):
    page = request.GET['page']
    if page in util.list_entries():
        return HttpResponseRedirect("wiki/" + page)
    else:
        if any([page in entry for entry in util.list_entries()]):
            entries = [entry for entry in util.list_entries() if page in entry]
            return render(request, "encyclopedia/index.html", {
                "entries": entries
            })
        return HttpResponseNotFound("Page not found")


def add(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            util.save_entry(
                form.cleaned_data["title"], form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("add"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewForm()
        })


def edit(request, page):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            util.save_entry(
                form.cleaned_data["title"], form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("page", args=[page]))

    return render(request, "encyclopedia/edit.html", {
        "page": page,
        "form": EditForm(
            {'title': page, "content": util.get_entry(page), }
        )
    })


def random(request):
    entries = util.list_entries()
    selected_page = choice(entries)
    return HttpResponseRedirect(reverse("page", args=[selected_page]))
