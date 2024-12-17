from django.shortcuts import render
from .models import Topic
from .forms import TopicForm

# Create your views here.
def index(request):
    """the main page of learning_logs"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """display all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """display single topic and all items of it"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """add new topic"""
    if request.method != 'POST':
        # didn't commit data: create a new from
        form = TopicForm()
    else:
        # POST commits data: process data
        form = TopicForm(date=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # display empty form or indicate form is unavailable
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
