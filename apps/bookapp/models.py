from django.db import models

# Create your models here.

class BooksClassify(models.Model):
    id = models.AutoField(primary_key=True)
    classify = models.CharField(max_length=32)

    class Meta:
        db_table = 'djgapp_booksclassify'
        verbose_name = '书籍分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.classify

class ScienceAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=32)
    brief = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'djgapp_scienceauthor'
        verbose_name = '科幻小说作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author

class ScienceBooks(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=32)
    brief = models.TextField(blank=True, null=True)
    author = models.ForeignKey(ScienceAuthor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'djgapp_sciencebooks'
        verbose_name = '科幻书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name

class ScienceBooksPageView(models.Model):
    id = models.IntegerField(primary_key=True)
    read_num = models.IntegerField(verbose_name='阅读量')
    comment_num = models.IntegerField(verbose_name='评论量')
    book = models.ForeignKey(ScienceBooks, on_delete=models.CASCADE)

    class Meta:
        db_table = 'djgapp_sciencebookpageview'
        verbose_name = '阅读量和评论量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.read_num

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=10)
    password = models.CharField(max_length=32)
    gmail = models.CharField(max_length=32)

    class Meta:
        db_table = 'djgapp_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.TextField(blank=True, null=True)
    brief = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'djgapp_author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author

class Books(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    brief = models.TextField(blank=True, null=True)
    mark = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        db_table = 'djgapp_books'
        verbose_name = "书籍"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.book_name)

class Book_PageView(models.Model):
    id = models.AutoField(primary_key=True)
    read_num = models.IntegerField(verbose_name='阅读量')
    comment_num = models.IntegerField(verbose_name='评论量')
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    class Meta:
        db_table = 'djgapp_pageview'
        verbose_name = '阅读量和评论量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.read_num

class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    chapter_name = models.TextField(blank=True, null=True)
    chapter_content = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    class Meta:
        db_table = 'djgapp_chapter'
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.chapter_name)