
from .models import Poll, Question, FinishedPoll, Answer, QuestionChoice
from rest_framework import serializers


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['name', 'date_start', 'date_end', 'description', 'questions', 'id']


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    class Meta:
        model = Question
        fields = ['text', 'question_type', 'id', 'choices']


class FinishedPollSerializer(serializers.ModelSerializer):
    answers = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = FinishedPoll
        fields = ['user_id', 'poll', 'id', 'answers']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['text', 'question', 'id', 'finished_poll']


class QuestionChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionChoice
        fields = ['text', 'question', 'id']
