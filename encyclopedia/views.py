from django.shortcuts import render

from . import util
import markdown

from django import forms
from django.shortcuts import redirect
# from django.urls import reverse

class SearchForm(forms.Form):
    query_term = forms.CharField(label='Search Nareklopedia', max_length=100) # this attribute must be the same as name='query_term' in html's <input name='query_term'> etc.

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
        query_term = form.cleaned_data['query_term']
        print(f'Search term: {query_term}')
        # return redirect('encyclopedia:entry', title=query_term)
        return entry(request, query_term)
    
    return index(request)

    


