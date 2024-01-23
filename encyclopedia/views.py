from django.shortcuts import render, Http404, redirect
import markdown2
import random

from . import util

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    # Retrieve the content of the entry based on the provided title.
    entry_content = util.get_entry(title)

    # Check if the entry exists
    if entry_content is not None:
        # Convert the Markdown content to HTML
        html_content = markdown2.markdown(entry_content)

        # Render the entry page and pass the title and HTML content to the template
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html_content": html_content,
        })
    else:
        # If the entry doesn't exist, raise error
        raise Http404("Entry not found")

def search(request):
    # Get the search query from the request's GET parameters (form in layout.html)
    query = request.GET.get("search_query", "")

    # Get a list of all existing encyclopedia entries
    entries = util.list_entries()

    # Check if there is an exact match (case-insensitive)
    if query.lower() in (entry.lower() for entry in entries):
        # Redirect to the entry page
        return redirect("entry", title=query)

    # If not, filter entries based on whether the query is a substring of each entry
    matching_entries = []
    for entry in entries:
        if query.lower() in entry.lower():
            matching_entries.append(entry)

    # Render a page with the results of the substrings
    return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "matching_entries": matching_entries,
        } )

def new_page(request):

    # Check if methos is POST and retrieve the info
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Check if an entry with the same title already exists
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new.html", {
                "message": "Entry already exists"
            })
        
        # Save the new entry
        util.save_entry(title, content)

        # Redirect to the new entry's page
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    
    # Retrieve the content of the entry based on the provided title.
    content = util.get_entry(title)

    # Handle form submission
    if request.method == "POST":

        # Get the updated content from the submitted form
        updated_content = request.POST.get("edit_content")

        # Save the updated content
        util.save_entry(title, updated_content)

        # Redirect to the entry's page after saving
        return redirect('entry', title=title)


    # Render a page with the initial content of the entry
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):

    # Get all entries
    entries = util.list_entries()

    # Choose randomly an entry
    random_entry = random.choice(entries)

    # Redirect to that entry
    return redirect('entry', title=random_entry)
