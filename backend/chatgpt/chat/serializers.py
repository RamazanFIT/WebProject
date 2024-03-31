from rest_framework import serializers
from .models import ChatGroup, ChatgptHistory


class ChatgptHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatgptHistory 
        fields = ['message', 'response_message']
    
class ChatGptSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
      
class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ['label']
        
class FullChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        # fields = '__all__'
        fields = ['id', 'label']