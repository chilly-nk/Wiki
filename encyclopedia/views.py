from django.shortcuts import render

from . import util
import markdown

from django import forms
from django.shortcuts import redirect
# from django.urls import reverse

# from django.contrib import messages
import os
from django.conf import settings

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Nareklopedia', max_length=100) # this attribute must be the same as name='query' in html's <input name='query'> etc.

class NewPageForm(forms.Form):
    title = forms.CharField(
        label='title', max_length=200, 
        widget=forms.TextInput(attrs={'placeholder': 'Title', 'style': 'width: 100%;'}))
    content = forms.CharField(
        label='content',
        widget=forms.Textarea(attrs={'name': 'content', 'rows': 10, 'cols': 50, 'placeholder': 'Enter your Wikipedia content here in markdown language.'}))
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        entries = util.list_entries()
        entries_lower = [entry.lower() for entry in entries]

        if title.lower() in entries_lower:
            exact_title_index = entries_lower.index(title.lower())
            exact_title = entries[exact_title_index]
            msg = f"A Wiki entry with title '{exact_title}' already exists."
            raise forms.ValidationError({'title': msg}) # to associate the error with the field
        
        return cleaned_data

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

def create(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            filename = '_'.join(title.split()).capitalize()
            filepath = os.path.join(settings.BASE_DIR, 'entries', f"{filename}.md")
            
            with open(filepath, 'w', encoding='utf-8') as md_file:
                md_file.write(f"# {title}\n {content}")
            
            return entry(request, filename)
        
        else:
            return render(request, 'encyclopedia/new_page.html', {
                'form': form,
            })
    
    return render(request, 'encyclopedia/new_page.html', {
        'form': NewPageForm(),
    })

    


