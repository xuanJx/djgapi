from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *
from .models import *

# Create your api views here.

class AuthorAPIView(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

class BooksAPIView(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializers
    filter_fields = ('id', 'book_name', 'author')
    search_fields = ('book_name', 'author')

    @action(methods=['GET'], detail=False)
    def mark(self, request):
        obj = Books.objects.filter(mark=request.GET['mark'])
        ser = BookSerializers(instance=obj, many=True)
        return Response(ser.data)

    @action(methods=['GET'], detail=False)
    def author(self, request):
        obj = Books.objects.filter(author=request.GET['author'])
        ser = BookSerializers(instance=obj, many=True)
        return Response(ser.data)


class ChapterAPIView(ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializers

    @action(methods=['GET'], detail=False)
    def book_id(self, request):
        obj = Chapter.objects.filter(book_id=request.GET['book_id'])
        ser = ChapterSerializers(instance=obj, many=True)
        return Response(ser.data)

class UserAPIView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class ScienceAuthorVPIView(ModelViewSet):
    queryset = ScienceAuthor.objects.all()
    serializer_class = ScienceAuthorSerializers

class ScienceBooksVPIView(ModelViewSet):
    queryset = ScienceBooks.objects.all()
    serializer_class = ScienceBooksSerializers

    @action(methods=['GET'], detail=False)
    def author_id(self, request):
        obj = ScienceBooks.objects.filter(author_id=request.GET['author_id'])
        ser = ScienceBooksSerializers(instance=obj, many=True)
        return Response(ser.data)



