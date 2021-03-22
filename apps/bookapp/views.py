from django.shortcuts import render
from .models import *

from string import ascii_lowercase


# Create your views here.

def chapter_content(request, pk):
    return render(request, 'bookapp/chapter-content.html')



def sciencebookpage(request, pk):
    return render(request, 'bookapp/sciencebook.html')

def originalpage(request):
    return render(request, 'bookapp/original.html')

def bookspage(request):
    return render(request, 'bookapp/books.html')

def bookpage(request, pk):
    return render(request, 'bookapp/book.html')

def authorspage(request):
    return render(request, 'bookapp/authors.html')

def loginpage(request):
    return render(request, 'bookapp/login.html')

def logoutpage(request):
    return render(request, 'bookapp/logout.html')

def registerpage(request):
    return render(request, 'bookapp/register.html')

def scienceauthor(request):
    return render(request, 'bookapp/scienceauthor.html')

def sciencebooks(request):
    return render(request, 'bookapp/sciencebooks.html')

def index(request):
    return render(request, 'bookapp/index.html')