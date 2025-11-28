from django.contrib import admin
from .models import Poll, Choice, Vote

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'expires_at']
    list_filter = ['status', 'created_at']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'choice', 'voter_identifier', 'voted_at']
