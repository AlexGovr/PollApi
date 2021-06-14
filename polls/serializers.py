
from .models import Poll, Question, FinishedPoll, Answer, Choice
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(required=False, queryset=Question.objects.all())
    class Meta:
        model = Choice
        fields = ['text', 'question', ]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)
    poll = serializers.PrimaryKeyRelatedField(required=False, queryset=Poll.objects.all())
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'id', 'poll', 'choices', ]
    
    def create(self, validated_data):
        try:
            choices_data = validated_data.pop('choices')
            question = super().create(validated_data)
            if validated_data.get('question_type', '') in (Question._ONE, Question._MANY):
                srl = ChoiceSerializer()
                for ch in choices_data:
                    srl.create({'question': question, **ch})
        except KeyError:
            question = super().create(validated_data)
        return question


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Poll
        fields = ['name', 'date_start', 'date_end', 'description', 'id', 'questions']
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        poll = super().create(validated_data)
        srl = QuestionSerializer()
        for q in questions_data:
            srl.create({'poll': poll, **q})
        return poll


class FinishedPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedPoll
        fields = ['user_id', 'poll', 'id', 'answers']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['text', 'question', 'id', 'finished_poll']

    def create(self, validated_data):
        poll_by_fpoll = validated_data['finished_poll'].poll
        poll_by_question = validated_data['question'].poll
        if poll_by_fpoll is not poll_by_question:
            raise serializers.ValidationError("question's and finished_poll's poll_id value must be the same")
        return super().create(validated_data)
