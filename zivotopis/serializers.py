from rest_framework import serializers
from .models import Post, Image, Email, GalleryItem, Ceny

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'text',
            'category',
            'created_date',
            'published_date',
            'images',
        ]
        read_only_fields = [
            'id',
            'author',
            'created_date',
            'published_date',
        ]   # alebo ['id', 'author', 'title', 'text', 'category', 'created_date', 'published_date', 'images']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['sender_name', 'sender_email', 'message', 'created_at']
        read_only_fields = ['created']

class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = ['id', 'title', 'image']
        

class CenySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceny
        fields = '__all__'
        
