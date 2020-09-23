from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class NewForm(forms.Form):
    class TitleField(forms.CharField):
        def validate(self, value):
            super().validate(value)
            if value in util.list_entries():
                raise ValidationError(f"ERROR: Title {value} already exists!")

    title = TitleField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, page):
    if page in util.list_entries():
        return render(request, "encyclopedia/page.html", {
            "page": page,
            "content": util.get_entry(page),
            "entries": util.list_entries()
        })
    else:
        return HttpResponseNotFound("Page not found")


def search(request):
    page = request.GET['page']
    if page in util.list_entries():
        return HttpResponseRedirect("wiki/" + page)
    else:
        return HttpResponseNotFound("Page not found")


def add(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("add"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewForm()
        })
