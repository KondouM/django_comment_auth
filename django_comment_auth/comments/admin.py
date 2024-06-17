from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'created_at', 'updated_at')
    
admin.site.register(Comment,CommentAdmin)
