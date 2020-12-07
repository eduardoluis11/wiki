from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# This will show the page defined on the "test.html" file. I need to add "test"
# in "urls.py". IT WORKS.
def test(request):
    return render(request, "encyclopedia/test.html")

