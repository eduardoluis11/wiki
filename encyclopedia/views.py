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

# This is a function that will allow me to redirect a user if they get a POST request (source: 
# https://www.fullstackpython.com/django-http-httpresponseredirect-examples.html )
from django.http import HttpResponseRedirect

""" This generates a seed so that the random number generator generates a number that is truly random 
(source: https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/ ). """
seed(1)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
        # This is a test to see if I can send an element from a python array into index.html. Turns out that
        # util.list_entries() generates an array.
        # "random_entry": util.list_entries()[randint(0, len(util.list_entries()) - 1)]
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
I want to raise a "404" error if "None" is returned (I will display the message "page not found".)

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

""" This function will redirect the user to a random entry if they click on "Random Page" on any page of the wiki.

I will redirect the user to "display_entry.html", since that the page that renders the entries. However, instead of 
taking the entry name from input from the user, I will randomly obtain an entry name by using the randint() function.

I also need to take the title of the entry and format it properly before rendering it.

I need to use len() to obtain the number of elements in a python array (source: 
https://www.askpython.com/python/array/array-length-in-python ).

"len(util.list_entries())" is a number which represents the number of elements in the python array
that contains all of the entries. However, remember that I start counting the number of elements at 0, 
so I need to stop counting the elements once I reach one minus the last element (that means, that 
if the array has 7 elements, the last element will be the 6th element). Otherwise, I get an error. 

So, I need to subtract 1 to len(util.list_entries()) to get 1 minus the total number of elements in the "entries"
array, so that I don't get out of range and so that I don't get any error messages. 

randint() will generate a random number between 0 and the number of elements in the array that contains all of the 
wiki's entries.
"""
def random_article(request):
        # This is a test to see if I can send an element from a python array into index.html. Turns out that
        # util.list_entries() generates an array.
        random_entry = util.list_entries()[randint(0, len(util.list_entries()) - 1)]

        # This will generate the article from the entry name obtained by the random generator
        article = markdown2.markdown(util.get_entry(random_entry))
        article_md_format = util.get_entry(random_entry)
        title = article_md_format.split('\n')[0]

        # This will remove the "# " characters from the title
        fixed_title = title.replace('# ', '')

        return render(request, "encyclopedia/display_entry.html", {
        "entries": article,
        "title": fixed_title
    })

""" This will make the user enter into an entry page if the type an existent entry name, or to a list of pages
with a name similar to what they typed on the search bar.

If I write anything on the search bar and I hit the Enter key, the URL of the site will change to 
“http://127.0.0.1:8000/?q=harvard”. I only want the text that’s after the “q=” (which, in this case, it’s “harvard”). 
Then, I will grab that text, and compare it to the existing entries of the wiki.

If the entry exists (I will use an “if” statement), I will take the user to that entry. I could do that by taking them 
to “/wiki/(text obtained from the text typed by the user on the search bar)”.

I will look for a python function that allows me to search for text from a string AFTER a specific character (in my 
case, after the “=” character from “?q=”). If I can't find any, I will simply delete “http://127.0.0.1:8000/?q=” by using 
the same python function that I used for part 1 to write the title of the entry on the browser’s tab.

It turns out that, indeed, such function exists (source: 
https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring).
However, remember that I will get the text from the search bar from a form, NOT from the URL (or at least, it’s not necessary 
to get it from the URL). I will simply see the HTML form where the search bar is created, and store that text into a variable. 
Then, I could take the user to “/wiki/(text from that variable)” to enter that entry’s page.

I found the form that contains that search bar. It’s a GET request (since the method is not explicitly typed, then it’s a 
GET request). The search bar form is in “layout.html”.

I need to look up (by looking at my code from Web 50’s 1st HW assignment, that is, the Google HW) how to grab text from a 
form after the user submits a form (or hits enter after filling in a form).

It turns out that I need to use the “action” attribute of the “<form>” tag to send the data from the form to anywhere 
else. However, I may need to look up a tutorial on how to work with forms, since I don’t know how to grab the text from a 
form to insert it into a variable (I could look up a search bar tutorial.)

Another method that I found is to obtain the data from the HTML form, and insert it into a variable by using Django. In 
my case, I will use the GET method. I could create a variable, and insert the following data in it: 
“request.GET.get('(name of the input tag that contains the text)')” (source: 
http://www.learningaboutelectronics.com/Articles/How-to-create-a-form-in-Django-using-plain-HTML.php .)

Then, I would insert that variable somewhere (like in the wiki_article() function) so that the page for that entry is 
displayed. I could use something like “wiki_article(query)” to render the page of that entry. Alternatively, I could 
use code similar to that of random_article, and simply insert the word from the user’s input instead of using “random_word”.

But, to do either of those methods, I need to add a new URL into urls.py (the url would have the format 
“/?q=(text typed by the user)” .)

After further testing, I decided that it was best to use a POST method for the form. Then, since the input name is 'q', 
I would use 'request.POST.get('q')' so  that I got the input typed by the user on the search bar, which uses a POST
method (source: http://www.learningaboutelectronics.com/Articles/How-to-create-a-form-in-Django-using-plain-HTML.php).

Now, I need to add an “if” statement to specify that, if the entry name exists, to send the user to that entry’s page.
Otherwise, something else must happen. In my case, that something else means displaying a list of entries that have at least 
one of the characters from the input typed by the user in their title.

Let me look at any of the previous functions. I think that, if I insert a word that is not an existing entry name, the 
list_entries() function returns “None”. So, I think I need to put “if None” if the user types a non-existent entry name, 
so that I display something else if the user types a non-existent entry name.

Yes, I need to use “if (condition) is None” if the user types a non-existent entry name, since the list_entries() 
function returns “None” if the user types an entry name that doesn’t exist.

First, I need to add an “if” statement to specify that, if the entry name exists, to send the user to that entry’s page. 
Otherwise, something else must happen. In my case, that something else means displaying a list of entries that have at 
least one of the characters from the input typed by the user in their title.

Let me look at any of the previous functions. I think that, if I insert a word that is not an existing entry name, the 
list_entries() function returns “None”. So, I think I need to put “if None” if the user types a non-existent entry name, 
so that I display something else if the user types a non-existent entry name.

Yes, I need to use “if (condition) is None” if the user types a non-existent entry name, since the list_entries() function 
returns “None” if the user types an entry name that doesn’t exist.

I’m going to use the string.find("substring") function to look up the substring typed by the user on the search bar, and to 
compare that to the existing entry titles (source: eldarerathis from
https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method .) If the substring matches 
any of the entry titles, I should display those entry titles. However, the function that I just mentioned works if I’m 
comparing one string and one substring. My string in this case would be the entry title.

The problem in this case is that the string is an array. That array contains the list of all of the existing entry titles. 
So, to turn that array into a single string, I will use a “for” loop, and the “array[i]” notation.

I should ideally put that directly in the “/query” page, which would be the display_entry.html. So, I would need to render 
everything that the “for” loop is creating directly into the display_entry.html page. So, I would need to send the 
“list_of_entries()” and “query” variables from query_search() function from the views.py file into the display_entry.html 
page.

And to avoid any conflicts with the if entries == 'not found'“” or “else” from the jinja notation in display_entry.html, 
I will create an extra condition in the jinja notation in display_entry.html file saying something like 
“elseif entries == ‘query search’”.

The util.list_entries() function generates me the array that has all of the titles of the existing entries. I will assign a 
name to that array, and then send it to display_entry.html. I also need to assign a name to the “query” variable before 
sending it to the display_entry.html file. I could just simply call it “query” though.

The “article” variable will have the value “query search” if the word typed by the user is a non-existent entry title. This 
will make display_entry.html to display a list of all of the entry titles that have that query as a substring.

I have another idea: I will use another 2 variables for the lowercase versions of “entry” and “query”, which I will only use 
for comparing the lowercase versions of each. I will do this to prevent the entry titles from being printed in lowercase 
letters. I will have to do this on the views.py file, and then send the lowercase variables into display_entries.html.

I couldn't fix the bug that prevent the user from finding entry titles if the entry title has upper case letters, but the
user only types lowercase letters in the search bar. If I try using regular expressions or turning the letters into lowercase, 
I either get an error, or I will print the entry titles in lowercase letters. So, the user will have to type uppercase
letters on the search bar if the entry title has uppercase letters in it.

I will make the entire process of getting the query typed by the user on the search bar, verifying that the query is a 
substring of an existent entry name, turning both things into lowercase letters, and obtaining the entire list of entry 
titles that have that substring in the views.py file. Then, I will store all of that data into an array, and send it into 
display_entry.html. Then, on display_entry.html, I will iterate that array to display all of the results into a list.

I could also create a counter that will tell me if there’s at least 1 result, or if there are no results. If there are no 
results, I could print a message saying “Sorry: there are no results.” Alternatively, I could simply use the len() function, 
and say that, if “len(array) = 0”, create a variable that says “Sorry, there are no results for that query”. Then, I would 
send that variable to the display_entry.html (and there wouldn't be a problem since, if there are no results, an empty 
screen would be rendered anyways.)
	
To append an element to a python array, I need to use the “.append” property (source: 
https://www.askpython.com/python/array/python-add-elements-to-an-array ).

I can’t use the “entries” variable to display the list of entry titles, since “entries” will be used for specifying 
display_entry.html that, instead of rendering 1 entry page, that a list of entries should be displayed. So, I will need a 
new variable to display the list of entry titles in display_entry.html.
"""
def query_search(request):
    query = request.POST.get('q')
    list_of_entries = util.list_entries()

    entry_titles = []	# Declaring array with results
    
    # Declaring variable with error message if no results are available
    results_message = '' 


    # This will display a list of entries that are similar to what the user typed on the search bar
    if util.get_entry(query) is None:
        article = 'query search'
        fixed_title = 'Search results'

        for entry in list_of_entries:
            if query.lower() in entry.lower():
                entry_titles.append(entry)		# Inserting each match into the results array

        if len(entry_titles) == 0:
            # Remember to use only one "=" when assigning text to a variable
	        results_message = 'Sorry, there are no results for that query.'

            # Debugging message
            # results_message = len(entry_titles) 

    else:
        article = markdown2.markdown(util.get_entry(query))
        article_md_format = util.get_entry(query)
        title = article_md_format.split('\n')[0]

        fixed_title = title.replace('# ', '')

    return render(request, "encyclopedia/display_entry.html", {
        "entries": article,
        "title": fixed_title,
        "entry_titles": entry_titles,
        "results_message": results_message
    })


""" I think it would be good if I created a new html file exclusively for creating a new page. Of course, 
I will inherit the styles from the layout.html file. Look at display_entry.html’s code to see how to inherit 
the code from layout.html.
    
Since I need to take the user to a new page, it would be a good idea to create a new html page. That is, it 
would be good to create a new html file. I will put it in the “templates” folder (or more specifically, I 
will put it in the “encyclopedia” folder.) 

To make the users go to a new page when clicking on the “Create New Page” text on the sidebar, I need to add 
a link to that text first. To do that, I need to add an <a> tag with an “href” attribute. It would also be a 
good idea to create a new link in the urls.py file to send the user to a new link once they click on 
“Create New Page”.

However, remember that, to create a new link on urls.py, I need to give it a function from the views.py file. 
Since I want an entirely new function for the page that lets you create an entry, I need to 1st create the 
function on views.py.

Since there are a ton of steps that I need to do before being able to render the creation page, I will make the 
page simple at first. I won’t display anything other than the sidebar and the title on the browser’s tab.

After writing the code on the views.py and urls.py files, I need to add the link towards “/create” in the href 
property of the “Create New Page” text on the sidebar, which is on the layout.html file.

The submit button already serves the function of saving the new page. The only problem is that, currently, I haven’t 
added the function to save the new entry to the website.

To save the newly created entry (the user should use markdown notation), I need to add a new function on the views.py 
file. I will give it a different name other than “save_entry()” to avoid any issues with the existing function. I will call 
the function “add_entry()”. I don’t need to add any parameters, since the title and the description of the entry will be 
sent to the save_entry() function, which already accepts 2 parameters (and it’s an existent function.) 
	
The new function that I’ll create will have 3 purposes: detect if the user has submitted the form from the create.html 
page, send the title and the description of the entry typed by the user to the save_entry() function, and redirect the 
user to the page of the newly created entry. To redirect the user to the newly created page, I could use code like 
‘f"wiki/{variable_with_the_title}"’.

First, to detect whether the user has hit the submit button from the “/create” page, I could use the same code as I did in 
the search algorithm. That is, I could use the “request.POST.get('name_of_the_input')” function. I would need to call it 
twice: once for the title, and once for the content of the entry. I will insert each of the calls of the request.POST.get() 
function into 2 separate variables.

Then, to create the entry and save it into the disk (that is, to save it into the website), I will call the save_entry(1st 
parameter, 2nd parameter) function, where the 1st and 2nd parameters will be the 2 variables that I just created to insert 
the title and the content of the entry typed by the user.

Finally, to redirect the user to the page of the newly created entry, I will use the return render() function, but where 
the link where I will be redirected will be “/wiki/variable_with_title_of_the_entry”. To do that, I could use Python’s 
“f” function, which will read variables if I insert them between “{}”. So, I would need to use code like this: 
return render(request, f"encyclopedia/wiki/{variable_with_entry_title}").

I had a mistake in my way of thinking: I actually need to redirect the user to the display_entry.html page, and I need to 
specify that I need to go to the page of the newly created page. That can be done by adding a variable in the render() 
function called “entries” (same as I had done previously whenever I call the display_entry.hmtl page), but I need to specify 
that entries will have the same value as the the “entry-title” variable (that is, the variable that gets the title of the 
entry from the “/create” page form.)

Also, since I don’t know a more efficient way of doing this, I will have to use the get_entry() function to get the newly 
created entry, get the title from it, and transform it from markdown to HTML (just like I did for the wiki_article() function).

To start making the code that saves an entry to the disk (and therefore, to the wiki), I need to leave the 
form in create.html without the "action" attribute (for the time being) (source: https://youtu.be/S44qx6DoIv4?t=16507 ). 
Then to detect if the user has clicked the submit button (so that it sends POST data from the form), I need to 
use an "if" statement with the "request.POST" function (source: arulmr's reply from 
https://stackoverflow.com/questions/16053865/handling-requests-in-django ). This will both detect if the form has 
been submitted, and it will pick up the data from the inputs with both the title and the description of the new entry.

BUG: if the user types a "#" in the title, the entry will be created, but it
will be impossible to enter into that entry's page (unless you use the "random" button). Also, the title of the newly
created entry won't display in <h1> text once the user enters into a newly created entry (even if they typed the title
without any "#"). In fact, the title won't even be displayed at all on the newly created entry page.

BUG FIX: The problem of the titles with "#" giving me trouble was that the markdown code should NOT be typed in the
"title" field of the creation form. Instead, it should be typed on the <textarea> tag, that is, on the "description" field.
Also, remember to leave an space between the title and the "#". Also, remember that I'm typing the title of the entry twice:
once on the "title" field of the creation form, and once on the "description" field. It should be typed on both the "title"
input, and on the 1st line of the "description" field. 

To show an error message if the user types the title of an already existing entry, I will use the util.get_entry() function 
at the beginning of the create() function to look up if the input typed by the user in the “title” field is the title of an 
already existing entry. If it is, I will display the error message. For the time being, I will keep the user in the 
create.html page if they type the title of an existing entry (that is, they won’t leave the page to see the error message).

Then, I will use an “if” statement on the create.html file to check if there was an error. If there is, I will display the 
error message.

I could use the “is not None” operand to specify that, if an entry exist, to execute some code (source:  Daniel Stutzbach’s 
reply from https://stackoverflow.com/questions/2710940/python-if-x-is-not-none-or-if-not-x-is-none .) This will be very 
similar to what I did in the wiki_article() function. That is, I will use “util.get_entry(title_typed_by_the_user)” and 
“is not None” to check if the title typed by the user is the name of the entry. If that condition checks, I will assign 
an error message to a variable.

Then, I will send that variable to create.html. Then, in create.html, I will specify that, if the value of that variable is 
an error message, I will print the error message (I think I will style it in red.) 

Since the util.get_entry() function wasn't obtaining the title typed by the user if I just inserted the "entry-title" 
variable, I ended up using request.POST.get('entry-title') to make it work. It's not efficient doing it this way, but
it works.

If the user types the name of an entry that doesn't exist, they will be taken into the display_entry.html page.
The body and the title of that page will be that of what was obtained from the "entry-title" and "entry-body" fields
from the creation form. The 'return render(request, "encyclopedia/display_entry.html"' code snippet will only 
be executed after the "else" statement, and will take the user directly to the page of the newly created entry.

The HttpResponseRedirect() function will allow me to redirect a user to another page, that is, the URL of the URL
bar will change (source: Willem Van Onsem's reply from 
https://stackoverflow.com/questions/56164972/cant-do-a-simple-redirect-after-post-request-in-django-using-httpresponseredir)
"""
def create(request):
    title = 'Create New Page'   # This prints "Create New Page" on the browser's 

    # This will store an error message if the user types an existing entry
    error_message = ''
    
    # Obtaining the title and the description from the form
    if request.POST:
        entry_title = request.POST.get('entry-title')
        entry_description = request.POST.get('entry-body')

        # This checks if the title of the entry already exists in the website
        if util.get_entry(request.POST.get('entry-title')) is not None:
            error_message = 'Error'
        
        # If the entry doesn't exist, I will create a new entry
        else: 

            # This saves the entry in the website
            util.save_entry(entry_title, entry_description)

            # Transforming the article from Markdown to HTML
            article = markdown2.markdown(util.get_entry(entry_title))

            # This splits the text and obtains the .md file’s title
            title = entry_description.split('\n')[0]

            # This will remove the "# " characters from the title
            fixed_title = title.replace('# ', '')

            # This will send the user the newly created enttry page right after clicking "Save"
            
            return HttpResponseRedirect(f"/wiki/{entry_title}")

    return render(request, "encyclopedia/create.html", {
        "title": title,
        "error_message": error_message,
    })


""" DO NOT USE. This doesn't work.
"""
# def add_page(request):

# 	# Obtaining the title and the description from the form
#     if request.POST:
#         entry_title = request.POST.get('entry-title')
#         entry_description = request.POST.get('entry-body') 

#         # This saves the entry in the website
#         util.save_entry(entry_title, entry_description)

#         # Transforming the article from Markdown to HTML
#         article = markdown2.markdown(util.get_entry(entry_title))

#         # This splits the text and obtains the .md file’s title
#         title = entry_description.split('\n')[0]

#         # This will remove the "# " characters from the title
#         fixed_title = title.replace('# ', '')

# 	# Redirecting the user to the newly created page
#     return render(request, "encyclopedia/display_entry.html", {
#         "entries": article,
#         "title": fixed_title,
#         "entry_title": entry_title,
#         "entry_description": entry_description
#     })


# def get_title(request):
#     return render(request, "encyclopedia/display_entry.html", {
#         "entries": util.list_entries()
#     })













