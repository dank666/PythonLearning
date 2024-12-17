"""define learning_logs's URL patern"""
from django.urls import path
from . import views
app_name = 'learning_logs'
urlpatterns = [
    # main page
    path('', views.index, name='index'),
    # display all topics
    path('topics/', views.topics, name='topics'),
    # display detailed page of one topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # add new topic
    psth('new_topic/', views.new_topic, name='new_topic'),
]
