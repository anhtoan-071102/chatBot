from rest_framework import serializers
from .models import Chat, Messages

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['message_type', 'content', 'created_at']
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Nội dung không được để trống.")
        return value
    
class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'messages']