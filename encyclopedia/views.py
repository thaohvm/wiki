from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect

from . import util

class NewForm(forms.Form):
    new = forms.CharField(label="New Title")

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
    return render(request, "encyclopedia/add.html", {
        "add": add,
    })


# def add(request):
#     if request.method == "POST":
#         form = NewTaskForm(request.POST)
#         if form.is_valid():
#             new = form.cleaned_data["task"]
#             request.session["entries"] += [entries]
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "encyclopedia/add.html", {
#                 "form": form
#             })
#     else:
#         return render(request, "encyclopedia/add.html", {
#             "form": NewTaskForm()
#         })