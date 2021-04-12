from django.shortcuts import render, redirect
from .models import *
from .forms import RegisterForm
from string import ascii_lowercase


# Create your views here.

def chapter_content(request, pk):
    return render(request, 'bookapp/chapter-content.html')

def register(request):
    r_form = RegisterForm()
    message = ''
    success = ''

    if request.method == 'POST':
        r_form = RegisterForm(request.POST)
        if r_form.is_valid():
            passwd1_get = r_form.cleaned_data['password1']
            passwd2_get = r_form.cleaned_data['password2']
            email_get = r_form.cleaned_data['email']
            user_get = r_form.cleaned_data['username']

            try:
                if passwd1_get == passwd2_get:
                    new_user = User.objects.create(user=user_get, password=passwd1_get, gmail=email_get)
                    success = '注册成功'
                    return redirect('djgapp:login-page')
                else:
                    message = '输入的密码不一致'
            except:
                message = '邮箱已被注册'

    content = {
        'r_form': r_form,
        'message': message,
        'success': success
    }

    return render(request, 'bookapp/register.html', content)


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