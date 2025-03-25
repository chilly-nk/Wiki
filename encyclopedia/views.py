from django.shortcuts import render

from . import util
import markdown

from django import forms
from django.shortcuts import redirect
# from django.urls import reverse

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Nareklopedia', max_length=100) # this attribute must be the same as name='query' in html's <input name='query'> etc.

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
    })

def entry(request, title):
    contents_raw = util.get_entry(title)
    if contents_raw == None:
        contents_raw = f"#Error: '{title.capitalize()}' not found\n\n From Wiki, chilly-nk's encyclopedia.\n\n Wiki does not have an article with this exact name. Please visit [Home](/wiki) to see all available articles."
        contents = markdown.markdown(contents_raw)
    else:
        contents = markdown.markdown(contents_raw)
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        'contents': contents,
    })

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query'].lower()
        entries = util.list_entries()
        entries_lower = [entry.lower() for entry in entries]    
        if query in entries_lower:
            return entry(request, query)
        else:
            partial_match = [entry for entry, entry_lower in zip(entries, entries_lower) if query in entry_lower]
            if len(partial_match) > 0:
                message = f"Sorry, we couldn't find an exact match for '{query}', but here are some similar items:"
            else:
                message = f"Sorry, we couldn't find any match for '{query}'."
            return render(request, 'encyclopedia/search_results.html', {
                'message': message,
                'partial_match': partial_match,
            })
    
    # return index(request)

    


