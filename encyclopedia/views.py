from django.shortcuts import render

from . import util
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    contents = markdown.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        'contents': contents,
    })

