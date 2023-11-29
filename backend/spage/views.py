from django.shortcuts import render
from django.http import Http404, HttpResponse
# Create your views here.

def index(request):
    return render(request, 'test.html')

randomstring = ["This is section 1.","This is section 2.", "This is section 3."]

def section(request, num):
    if num <= 3:
        return render(request,"waitpage.html")
    else:
        raise Http404('No such section')
