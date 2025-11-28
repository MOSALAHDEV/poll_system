from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Count
from django.utils import timezone
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer, PollResultSerializer

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.action == 'list':
            return Poll.objects.filter(status='OPEN', expires_at__gt=timezone.now())
        return Poll.objects.all()
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def vote(self, request, pk=None):
        poll = self.get_object()
        serializer = VoteSerializer(data=request.data, context={'poll': poll})
        
        if serializer.is_valid():
            choice = Choice.objects.get(id=serializer.validated_data['choice_id'])
            Vote.objects.create(
                poll=poll,
                choice=choice,
                voter_identifier=serializer.validated_data['voter_identifier']
            )
            return Response({'message': 'Vote recorded successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def results(self, request, pk=None):
        poll = self.get_object()
        results = Vote.objects.filter(poll=poll).values('choice__text').annotate(votes=Count('id'))
        
        data = [{'choice': r['choice__text'], 'votes': r['votes']} for r in results]
        serializer = PollResultSerializer(data, many=True)
        
        return Response({
            'poll': poll.title,
            'total_votes': Vote.objects.filter(poll=poll).count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        poll = self.get_object()
        poll.status = 'CLOSED'
        poll.save()
        return Response({'message': 'Poll closed successfully'})
