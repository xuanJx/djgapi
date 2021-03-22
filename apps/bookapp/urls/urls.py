from django.urls import path
from bookapp import views

app_name = 'djgapp'

urlpatterns = [
    path('books/', views.bookspage, name='books-page'),
    path('book/<int:pk>/', views.bookpage, name='book-page'),
    path('authors/', views.authorspage, name='authors-page'),
    path('login/', views.loginpage, name='login-page'),
    path('logout/', views.logoutpage, name='logout-page'),
    path('register/', views.registerpage, name='register-page'),
    path('scienceauthor/', views.scienceauthor, name='scienceauthor-page'),
    path('sciencebooks/', views.sciencebooks, name='sciencebooks-page'),
    path('index/', views.index, name='index-page'),
    path('original/', views.originalpage, name='original-page'),
    path('sciencebook/<int:pk>/', views.sciencebookpage, name='sciencebook-page'),
    path('content/<int:pk>/', views.chapter_content, name='content-page')
]

