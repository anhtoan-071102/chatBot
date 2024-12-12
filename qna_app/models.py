from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat")
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Chat {self.id}"
    
class Messages(models.Model):
    MESSAGE_TYPE = [
        ('question', 'Question'),
        ('answer', 'Answer'),
    ]
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,related_name="messages")
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}..."
