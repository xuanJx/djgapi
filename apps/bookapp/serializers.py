from rest_framework import serializers
from .models import *

# Create your serializers here.

class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class ChapterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

