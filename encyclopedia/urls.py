from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # If the user types "127.0.0.1/test", they will see "hello world". See "views.py" for more
    # details on what "test" shows. IT WORKS.
    path("test", views.test, name="test"),

    # This url will send the user to the wiki entry for the "CSS" article. See the "wiki_entry" function from
    # the "views.py" file for more details. IT WORKS. The problems I was getting were with the "views.py" file,
    # NOT with this file.
    path("wiki", views.wiki_article, name="wiki_article"),
]
