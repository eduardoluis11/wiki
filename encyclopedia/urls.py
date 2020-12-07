from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # If the user types "127.0.0.1/test", they will see "hello world". See "views.py" for more
    # details on what "test" shows. IT WORKS.
    path("test", views.test, name="test")
]
