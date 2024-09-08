from rest_framework import serializers
from .models import Author, Book
from datetime import date

class AuthorSerializer(serializers.ModelSerializer):
    # the name field to store the name from the client side
    name = serializers.CharField()

    class Meta:
        model = Author
        fields = ['name']

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    # Nested author serializer to include related author info
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__' # Serializes all fields of the Book model, including 'author'

    # Custom validation to ensure publication year is not in the future
    def validate_publication_date(self, value):
        if value > date.today().year:
            raise serializers.ValidationError("The publication date cannot be in the future.")
        return value
    
    def create(self, validated_data):
        # Extract nested author data
        author_data = validated_data.pop('author')

        # Create the author
        author, created = Author.objects.get_or_create(**author_data)

        # Create the book with the newly created or retrieved author
        book = Book.objects.create(author=author, **validated_data)

        return book
    
    def update(self, instance, validated_data):
        # Extract nested author data
        author_data = validated_data.pop('author', None)

        # Update the author if provided
        if author_data:
            author, created = Author.objects.get_or_create(**author_data)
            instance.author = author

        # Update the rest of the Book instance fields
        instance.title = validated_data.get('title', instance.title)
        instance.publication_year = validated_data.get('publication_year', instance.publication_year)

        instance.save()
        return instance

# The author field in the BookSerializer is a nested serializer that uses the AuthorSerializer to 
# handle the relationship between the Book and Author models. This means that whenever you serialize a Book,
# the related Author information will also be serialized as part of the Book object. For example, the author's 
# name will be included in the serialized response for a book.