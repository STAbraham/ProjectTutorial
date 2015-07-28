from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from polls.models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice']) # Remember: Form submits choice=# as a dictionary
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form. STA -- seems like it stays on the polls/<question_id>/vote/ url though
        return render(request, 'polls/detail.html', {'question': p, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after succesfully dealing with
        # POST data. This prevents data from being posted twice if a user hits
        # the BACK button
        return HttpResponseRedirect(reverse('polls:results', args=(p.id, )))

""" Old implementation of views before the introduction of geneneric views for index, detail and results

def index(request):
    context_dict = {}
    context_dict['latest_questions'] = Question.objects.order_by("-pub_date")[:5]
    return render(request, 'polls/index.html', context_dict)

def detail(request, question_id):
    # Default Primary Key assigned my PSQL used as question id
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results (request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""