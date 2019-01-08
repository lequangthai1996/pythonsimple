from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Board, Post, Topic
from django.contrib.auth.models import User
from .forms import NewTopicsForm, PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicsForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                messages=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk = topic.pk )
    else:
        form = NewTopicsForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic })

def reply_topic(request, pk, topic_pk):
  topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.topic = topic
      post.created_by = request.user
      post.save()
    return redirect('topic_posts', pk = pk, topic_pk = topic_pk)
  else:
    form = PostForm()
  return render(request, 'reply_topic.html', {'topic': topic, 'form': form})