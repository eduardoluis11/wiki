from django.urls import path

from . import views

""" If the user clicks on "Random Page" on any page, they will be taken to the "URL/random" page, 
which will display a random article from the existing entries on the wiki (source: 
https://stackoverflow.com/questions/62797803/select-an-random-page-with-django ). "random_article"
will be a python function from views.py, which is where I need to send the user if they enter
to the "/random" URL.

To send the user to the "random_article" function in the views.py file, so that they can then be sent to 
a random entry page, I need to put "views.random_article" and 'name="random_article"' in the 'path'
attribute (source: https://youtu.be/pRNhdI9PVmg?t=10108 .) 

The 'query' URL refers to when the user makes a search in the search bar, and presses the Enter key. This will 
send the user to an entry page if the type an existent entry name in the search bar. The reason why I'm not
typing it in the format '?q=(text)' is because I decided to give a POST method to the search form so that
nothing appears on the URL bar. Instead, when the user types anything into the search bar and presses enter, 
I will redirect them to a a link with the format '/query' (source: 
https://stackoverflow.com/questions/62797803/select-an-random-page-with-django). 

The "/create" URL will send the user to the create() function from views.py, which will send the user to the page
that allows them to create an entry for the wiki.

I added a new URL called 'created-article', which will activate the create_article() function from views.py (so
that a new article can be added to the website.)
"""
urlpatterns = [
    path("", views.index, name="index"),

    # If the user types "127.0.0.1/test", they will see "hello world". See "views.py" for more
    # details on what "test" shows. IT WORKS.
    path("test", views.test, name="test"),

    # This url will send the user to the wiki entry for the "CSS" article. See the "wiki_entry" function from
    # the "views.py" file for more details. IT WORKS. The problems I was getting were with the "views.py" file,
    # NOT with this file.

    # Now, I will use "<str:entry>" so that, when the user types "127.0.0.1/CSS" or "127.0.0.1/Git"m the will go
    # to the CSS or Git wiki article, respectively. This may fail though. I need to put "entry" in "views.py".
    # IT WORKED PERFECTLY. Source: https://docs.djangoproject.com/en/3.1/topics/http/urls/ .

    # Now, I will modify this so that the URL format is "127.0.0.1/wiki/TITLE" (just like the homework asks me to.)
    # IT WORKS.
    # I will change the word "entry" by "word" in "<str:" so that I don't get confused by using the word "entry" so
    # much. Now, I need to go to "views.py", and put the word "word".
    path("wiki/<str:word>", views.wiki_article, name="wiki_article"),
    path("random", views.random_article, name="random_article"),
    path("query", views.query_search, name="query_search"),
    path("create", views.create, name="create")
]
