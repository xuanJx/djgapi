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

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ScienceAuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScienceAuthor
        fields = '__all__'

class ScienceBooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScienceBooks
        fields = '__all__'

