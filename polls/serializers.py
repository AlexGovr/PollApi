
from rest_framework.exceptions import ValidationError
from .models import Poll, Question, FinishedPoll, Answer, Choice
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'question', 'id', ]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)
    # poll = serializers.PrimaryKeyRelatedField(required=False, queryset=Poll.objects.all())
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'id', 'poll', 'choices', ]
    
    def create(self, validated_data):
        print('here')
        try:
            choices_data = validated_data.pop('choices')
            print(choices_data)
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
    # choices = AnswerChoiceSerializer(many=True)
    choices = serializers.PrimaryKeyRelatedField(many=True, queryset=Choice.objects.all())
    class Meta:
        model = Answer
        fields = ['text', 'question', 'id', 'finished_poll', 'choices', ]

    def run_validation(self, data):
        validated_data = super().run_validation(data=data)
        question = validated_data['question']
        text = validated_data['text']
        choices = validated_data['choices']

        if question.question_type == Question._TEXT:
            if not text:
                raise ValidationError({'text': 'this value must not be empty for "text" question_type'})
            validated_data['choices'] = []
        
        else:
            if question.question_type == Question._ONE:
                if len(choices) != 1:
                    raise ValidationError({'choices': 'there must be exactly one '
                                                    'choice for "choose_one" question_type'})
                choice_ids = tuple(question.choices.all())
                if choices[0] not in choice_ids:
                    raise ValidationError({'choices': 'choice must one of question.choices ids'})

            if question.question_type == Question._MANY:
                if len(choices) == 0:
                    raise ValidationError({'choices': 'there must be at least one '
                                                    'choice for "choose_many" question_type'})
                choice_ids_set = set(question.choices.all())
                if set(choices) - choice_ids_set:
                    raise ValidationError({'choices': 'choices must form a subset of question.choices ids'})
            
            validated_data['text'] = ''

        return validated_data
