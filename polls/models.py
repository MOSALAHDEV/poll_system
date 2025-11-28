from django.db import models
from django.utils import timezone

class Poll(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    
    def is_active(self):
        return self.status == 'OPEN' and self.expires_at > timezone.now()
    
    def __str__(self):
        return self.title

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return self.text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter_identifier = models.CharField(max_length=255)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('poll', 'voter_identifier')
    
    def __str__(self):
        return f"{self.voter_identifier} voted on {self.poll.title}"
