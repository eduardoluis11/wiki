from django.shortcuts import render

from . import util

# This will let me use "markdown", the package that converts Markdown into HTMl, so that the 
# text from the entry file is properly displayed instead of having the werid spaces, and so 
# the "#" characters convert the Markdown text into bold or italics when displayed in the web app
# (source: https://github.com/trentm/python-markdown2). 
import markdown2

# This will allow me to show a "404: page not found" error.
# Source: https://docs.djangoproject.com/en/3.1/intro/tutorial03/
from django.shortcuts import get_object_or_404

# This will allow me to use the function that shows the "404: Page not found" error.
# Source: https://docs.djangoproject.com/en/3.1/intro/tutorial03/ .
from django.http import Http404

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

If the word stored in "entry" is not one of the wiki's entries, the "get_entry()" function will return "None". 
I want to raise a "404" error if "None2 is returned (I will display the message "page not found".)

I changed the word "entry" by "word" in both the function wiki_article() and on "util.get_entry(word)" so that I know
that that word is the one being typed by the user (the one obtained by "<str:" in urlpatterns.)

To properly convert from Markdown into HTML so that the entry text doesn't have any weird space between 
each letter, and so that the "#" characters are able to make the text bold or italices (as it should in Markdown
format), I will use the "markdown.markdown(ENTRY_TEXT_VARIABLE)" function from the markdown2 package 
(source: https://github.com/trentm/python-markdown2 .)
"""
def wiki_article(request, word):
    # I will get the word from "<str:" from urlpatterns from urls.py by assigning a variable and using the
    # util.get_entry() function. This will let me to easily manipulate the word obtained.
    article = markdown2.markdown(util.get_entry(word))

    # If I insert the wrong word (that is, a non-existent wiki entry) into "wiki/article_name" while typing on the URL,
    # Django/Python will return "None" (like "Null" in other languages). Therefore, "article" will be "None" if I type
    # the wrong word in the url article, this will execute. THIS WORKED.
    if article is None:
        # This will show the "This page does not exist" error message.
        raise Http404("This page does not exist.")

    # This will return an error message if the user enters a wrong name for an entry (that is, if "entry" returns
    # "None")
    # Source: https://docs.djangoproject.com/en/3.1/intro/tutorial03/
    # question = get_object_or_404(entry)
    # try:
    #     message = util.get_entry(entry)
    # except None:
    #     raise Http404("This page does not exist")

    # If the user types the right article name (be it because it's one of the 6 entries that came by default with
    # this source code, or be it because the user created a new article), this will send the user to that wiki article.
    #
    # I created a file called "display_entry.html", which is where I will redirect the user if they type an
    # existing entry name. There, I have a template (like layout.html), but that I will only use to show each entry.
    return render(request, "encyclopedia/display_entry.html", {
        # I will use the word "word" instead of "entry" to know that this word is the one being obtained from
        # urlpatterns from "urls.py". IT WORKS PERFECTLY.

        # The word between quotation marks needs to be "entries" or won't work. I think that's because "entries" is the
        # name of the folder that contains all of the articles as ".md" files.
        #
        # I will insert here the "article" variable (the word typed by the user on the URL bar.) This seems to be like
        # sanitizing data in PHP.
        "entries": article 
    })

# def get_title(request):
#     return render(request, "encyclopedia/display_entry.html", {
#         "entries": util.list_entries()
#     })















