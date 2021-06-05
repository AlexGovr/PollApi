from django.urls import include, path
from rest_framework import routers
from polls.views import PollViewSet, QuestionViewSet, FinishedPollViewSet, AnswerViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'poll', PollViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'finished_poll', FinishedPollViewSet)
router.register(r'answer', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
