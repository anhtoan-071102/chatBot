from django.contrib import admin
from .models import Chat, Messages

# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    
@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'message_type', 'content', 'created_at')