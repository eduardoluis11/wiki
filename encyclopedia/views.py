from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


"""
This will show the page defined on the "test.html" file. I need to add "test"
in "urls.py". IT WORKS. 

The "encyclopedia" in "encyclopedia/test.html" refers to the folder named "encyclopedia" within the "templates" folder.
So, if I want to redirect the user to "entries", I would need to create an "entries" folder inside the "templates"
folder. HOWEVER, since I can just call the entries by using the function "get_entry" from util.py, I don't need
to redirect the user to "CSS.md" (nor the rest fo the entries.) Just look at the "index" function above me, and I will 
modify it so that I use the "get_entry" function to go to the "CSS.md" entry.
"""


def test(request):
    return render(request, "encyclopedia/test.html")


"""
This will render the CSS wiki entry. To do that, I will use the "get_entry" function from util.py. It seems that
it will be displayed on the index.html file, so that may give me an error. 

I need to go to "urls.py" from the "encyclopedia" folder, and add a path to show this (like "wiki"). IT WORKS. 
I needed to put "CSS" between quotation marks to make it work.

Now, I need to edit it so that it detects the name of ANY of the entries (CSS, Django, Git, etc.) I think that this
tutorial from freecodecamp may help me: https://www.youtube.com/watch?v=F5mRW0jo-U4&t=11061s .

I'm adding the word "entry" to see if, instead of "CSS", the "get_entry" will grab the user input on the url 
(see "urls.py" in the encyclopedia directory for more info.) That is, if the user types "127.0.0.1/CSS" or 
"127.0.0.1/Django", the user will enter into the CSS and the Django wiki entries, respectively. The "entry" variable
is grabbing a word from "urls.py"m which is grabbing a word from the URL which is being typed by the user. IT WORKED.
Source: https://docs.djangoproject.com/en/3.1/intro/tutorial03/ 
"""
def wiki_article(request, entry):
    return render(request, "encyclopedia/index.html", {
        "entries": util.get_entry(entry)
    })

















