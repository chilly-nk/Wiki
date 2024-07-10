from django.shortcuts import render

from . import util
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    contents_raw = util.get_entry(title)
    if contents_raw == None:
        contents_raw = f"#Error: '{title}' not found\n\n From Wiki, chilly-nk's encyclopedia.\n\n Wiki does not have an article with this exact name. Please visit [Home](/wiki) to see all available articles."
        contents = contents = markdown.markdown(contents_raw)
    else:
        contents = markdown.markdown(contents_raw)
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        'contents': contents,
    })

