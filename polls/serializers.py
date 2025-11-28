from rest_framework import serializers
from .models import Poll, Choice, Vote
from django.utils import timezone

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    
    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'created_at', 'expires_at', 'status', 'choices']
        read_only_fields = ['created_at', 'status']
    
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)
        return poll

class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()
    voter_identifier = serializers.CharField(max_length=255)
    
    def validate(self, data):
        poll = self.context['poll']
        
        if not poll.is_active():
            raise serializers.ValidationError("This poll is closed or expired.")
        
        if not Choice.objects.filter(id=data['choice_id'], poll=poll).exists():
            raise serializers.ValidationError("Invalid choice for this poll.")
        
        if Vote.objects.filter(poll=poll, voter_identifier=data['voter_identifier']).exists():
            raise serializers.ValidationError("You have already voted on this poll.")
        
        return data

class PollResultSerializer(serializers.Serializer):
    choice = serializers.CharField()
    votes = serializers.IntegerField()
