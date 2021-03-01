from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import *

# Create your api views here.

class AuthorView(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

class BooksView(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializers

class ChapterView(ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializers