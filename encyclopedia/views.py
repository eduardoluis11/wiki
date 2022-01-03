from django.shortcuts import render
from django.core.files.storage import default_storage   # This imports the default_storage() function

""" These two libraries will allow me to use the randint() function and to generate a seed. This way, I'll
be able to generate a random number, and to make sure that the number is truly random (source:
https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/ ). """
from random import randint
from random import seed

""" This will allow me to only extract the name of the .md file from a PATH. Source: 
https://www.techiedelight.com/get-filename-without-extension-python/ """
import os

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

""" This generates a seed so that the random number generator generates a number that is truly random 
(source: https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/ ). """
seed(1)

""" I need to use len() to obtain the number of elements in a python array (source: 
https://www.askpython.com/python/array/array-length-in-python ).

"len(util.list_entries())" is a number which represents the number of elements in the python array
that contains all of the entries. However, remember that I start counting the number of elements at 0, 
so I need to stop counting the elements once I reach one minus the last element (that means, that 
if the array has 7 elements, the last element will be the 6th element). Otherwise, I get an error. 

So, I need to subtract 1 to len(util.list_entries()) to get 1 minus the total number of elements in the "entries"
array, so that I don't get out of range and so that I don't get any error messages. 

randint() will generate a random number between 0 and the number of elements in the array that contains all of the 
wiki's entries.

NOTE: all of this will only work on index.html. However, I need to make the user to be able to go to a random 
entry page from any page within the website, NOT only from the index.html page."""
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
        # This is a test to see if I can send an element from a python array into index.html. Turns out that
        # util.list_entries() generates an array.
        "random_entry": util.list_entries()[randint(0, len(util.list_entries()) - 1)]
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
    # article = markdown2.markdown(util.get_entry(word))

    # If I insert the wrong word (that is, a non-existent wiki entry) into "wiki/article_name" while typing on the URL,
    # Django/Python will return "None" (like "Null" in other languages). Therefore, "article" will be "None" if I type
    # the wrong word in the url article, this will execute. THIS WORKED.
    """ To display an error message of 'Page not found', and avoid the error message saying "Type Error", 
    I added an if statement that checks if the entry exists. If it doesn't exist, I will get a "None" type.
    In that case, I will 'break the loop' to avoid getting the "Type Error", and I will assign a custom value
    to the "article" variable to tell display_entry.html to display an error message using <h1> and <p> tags.
    
    And, if the entry exists, I will simply insert the entry text as HTML into the "article" variable.

    Since the value being returned by get_entry() is an f.read(), which is an opened file, I will use the ".name"
    property to get the name of that file, which I will use as the title for that entry.

     After further consideration, I won't obtain the title using the filename, since I would need a library that 
    seems to be exclusive for Windows machines.

    To get the title, I may use a regular expression. I may read the 1st line of the text from the “entries” variable, 
    which is where the title with the correct casing is stored. So, I will read that 1st line, and I will stop reading 
    once I find a line break (\n). I don’t want the “#” sign either. So, I could try using a regular expression that 
    checks for a word on the “entries” variable that starts at the space after the “#” sign, and ends at the first “\n” 
    on the 1st line.

	I don’t want to get the title by reading the filename since I would need to use a library that’s for Windows machines. 
    So, if the code were stored or rendered on a Mac, the title would have every letter in lower-case. So, using the win32 
    library is not a universal solution.

	I could use a function in Python that splits all the text and inserts it into an array, which, in my case, it would be 
    the split() function (source: https://www.codegrepper.com/code-examples/python/extract+text+before+specific+word+python ). 
    Each section of the text would be inserted as an element of that array. The character that would be used for splitting 
    the entry text would be the line break, that is, “\n”. 

    However, the problem with suing split() as I mentioned in the previous paragraph is that I will also grab the “#” sign 
    and a space alongside teh title (i.e: I will grab “# CSS” instead of “CSS”). So, I need to remove the first 2 characters 
    (“#” and the space). To do this, I will use the replace() function from Python (source: 
    https://www.journaldev.com/23674/python-remove-character-from-string .)
	
    I will replace the “# ” from the title by an empty space to remove it by using the replace() function.

    I will assign an error message to both the "article" and "fixed_title" variables so that, if the user types a wrong
    entry on the URL, I won't get an error message from Django (with the yellow background). Instead, I will get a
    "Page Not Found" message on the browser's tab, and a custom error message that I made using <h1> and <p> as 
    the entry.  
    """
    if util.get_entry(word) is None:
        # This will show the "This page does not exist" error message using a Django template. I don't
        # want to use this any longer since I prefer showing a simpler error message using <h1> and <p> tags.
        # raise Http404("This page does not exist.")
        article = 'not found'
        fixed_title = 'Page Not Found'
    else:
        # I will get the word from "<str:" from urlpatterns from urls.py by assigning a variable and using the
        # util.get_entry() function. This will let me to easily manipulate the word obtained.
        article = markdown2.markdown(util.get_entry(word))

        """ I will use this to get the "#" sign instead of transforming that sign into an <h1> tag. I will do this
        to extract the title of the md file. """
        article_md_format = util.get_entry(word)

        # This will store the name of the .md file from which I'm getting the entry.
        # file = default_storage.open(f"entries/{word}.md")

        """ These two lines will get the name of the file from the PATH of the .md file that has the text for the 
        current entry, which is what I want to use as the title (source: 
        https://stackoverflow.com/questions/323515/how-to-get-the-name-of-an-open-file/324326 .) The problem with
        this is that the text is always being converted into lowercase. I want to have upper-case and lower-case 
        letters if the original name of the file hs both upper and lower case letters. 
        """
        # This splits the text and obtains the .md file’s title
        title = article_md_format.split('\n')[0]

        # This will remove the "# " characters from the title
        fixed_title = title.replace('# ', '')

        # file_name = file.name
        # title = os.path.basename(file_name)

        # title = util.get_entry(word).name


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
    """ I will also return the title of the text file that contains that entry (since I will use that as the title
    of the article, which will show up on the browser's tab.) """
    return render(request, "encyclopedia/display_entry.html", {
        # I will use the word "word" instead of "entry" to know that this word is the one being obtained from
        # urlpatterns from "urls.py". IT WORKS PERFECTLY.

        # The word between quotation marks needs to be "entries" or won't work. I think that's because "entries" is the
        # name of the folder that contains all of the articles as ".md" files.
        #
        # I will insert here the "article" variable (the word typed by the user on the URL bar.) This seems to be like
        # sanitizing data in PHP.
        "entries": article,
        "title": fixed_title
    })

# def get_title(request):
#     return render(request, "encyclopedia/display_entry.html", {
#         "entries": util.list_entries()
#     })















