from django.shortcuts import render

# Create your views here.


def index(request):
    print("da vao day")
    return render(request, "comment/index.html")