
from .models import Poll, Question, FinishedPoll, Answer
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

    def create(self, validated_data):
        print(validated_data)
        poll_by_fpoll = validated_data['finished_poll'].poll
        poll_by_question = validated_data['question'].poll
        if poll_by_fpoll is not poll_by_question:
            raise serializers.ValidationError("question's and finished_poll's poll_id value must be the same")
        return super().create(validated_data)
