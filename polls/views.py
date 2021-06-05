
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import FinishedPoll, Poll, Question, Answer
from .serializers import PollSerializer, QuestionSerializer, FinishedPollSerializer, AnswerSerializer


class BasicViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.not_auth_response()
        try:
            super().destroy(request, *args, **kwargs)
            # override default response as it may raise ConnectionResetError
            return Response({'status': 'successfuly deleted'})
        except Exception as e:
            return Response({'error': str(e)})

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.not_auth_response()
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)})

    def not_auth_response(self):
        return Response({'status': 'rejected: not authenticated'})

    def get_instance(self, id_):
        return self.queryset(id=id_)


class PollViewSet(BasicViewSet):
    queryset = Poll.objects.all().order_by('-date_start', ).reverse()
    serializer_class = PollSerializer


class QuestionViewSet(BasicViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class FinishedPollViewSet(viewsets.ModelViewSet):
    '''viewset will only return answers for user specified in request data'''
    queryset = FinishedPoll.objects.none()
    serializer_class = FinishedPollSerializer

    @action(detail=False, url_path='show')
    def list_mypolls(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        if not user_id:
            return Response({'details': 'user id is needed'})
        self.queryset = FinishedPoll.objects.filter(user_id=user_id)
        
        return super().list(request, *args, **kwargs)


class AnswerViewSet(viewsets.ModelViewSet):
    '''viewset will only return answers for finished poll specified in request data'''
    queryset = Answer.objects.none()
    serializer_class = AnswerSerializer

    @action(detail=False, url_path='show')
    def list_mypolls(self, request, *args, **kwargs):
        fpoll_id = request.data.get('finished_poll_id')
        if not fpoll_id:
            return Response({'details': 'finished_poll_id is needed'})
        self.queryset = Answer.objects.filter(finished_poll=fpoll_id)

        return super().list(request, *args, **kwargs)
