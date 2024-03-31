from django.db import models
from users.models import User


class ChatGroup(models.Model):
    label = models.CharField(max_length=255)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_id',
    )

class ChatgptHistory(models.Model):
    user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='userId',
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=2000)
    response_message = models.CharField(max_length=2000)
    chat_group = models.ForeignKey(
        to=ChatGroup,
        on_delete=models.CASCADE,
        related_name='message',
    )
    
    

