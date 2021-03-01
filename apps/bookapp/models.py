from django.db import models

# Create your models here.

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.TextField(blank=True, null=True)
    books = models.TextField(blank=True, null=True)
    mark = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.author

class Books(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    brief = models.TextField(blank=True, null=True)
    mark = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return str(self.book_name)

class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    chapter_name = models.TextField(blank=True, null=True)
    chapter_content = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.chapter_name)