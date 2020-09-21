from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from . import util


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