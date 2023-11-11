from django.db import models
from account.models import User
import uuid


class Message(models.Model):
    content = models.TextField()
    is_agent = models.BooleanField(default=False)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )

    def created_at_formatted(self):
        return self.created_at.strftime('%H:%M')

    def __str__(self) -> str:
        return self.content


class Chat(models.Model):
    CHOICES_STATUS = (
        (0, 'Ожидает'),
        (1, 'Активен'),
        (2, 'Закрыт'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sk = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(User, related_name='chat', on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE, null=True, blank=True)
    messages = models.ManyToManyField(Message)
    status = models.IntegerField(choices=CHOICES_STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def last_message(self):
        return self.messages.last()

    def __str__(self) -> str:
        return self.created_at.strftime('%H:%M %d.%m.%Y')
