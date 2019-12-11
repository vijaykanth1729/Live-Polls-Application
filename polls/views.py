import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count

from django.http import  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import PollForm, EditPollForm, ChoiceForm
from .models import Poll, Choice, Vote


def home(request):
    return render(request, 'polls/home.html')


@login_required
def list_polls(request):
    polls = Poll.objects.all()
    search_term = ''

    if 'text' in request.GET:
        polls = polls.order_by('text')

    if 'pub_date' in request.GET:
        polls = polls.order_by('-pub_date')
    if 'num_votes' in request.GET:
        polls = polls.annotate(Count('vote')).order_by('-vote__count')

    if 'owner' in request.GET:
        polls = polls.filter(owner=request.user)

    if 'search' in request.GET:
        search_term = request.GET['search']
        polls = polls.filter(text__icontains=search_term)

    paginator = Paginator(polls, 7)  # Show 5 polls per page

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

    context = {
        'polls': polls,
        'params': params,
        'search_term': search_term,
    }
    return render(request, 'polls/polls_list.html', context)


@login_required
def add_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.owner = request.user
            new_poll.save()
            choice1 = Choice(
                poll=new_poll,
                choice_text=form.cleaned_data['choice1']
            ).save()
            choice2 = Choice(
                poll=new_poll,
                choice_text=form.cleaned_data['choice2']
            ).save()
            messages.success(request,
                             'Poll and choice added successfully!',
                             extra_tags='alert alert-success alert-dismissable fade show')
            return redirect('polls:list')
    else:
        form = PollForm()
    context = {'form': form}
    return render(request, 'polls/add_poll.html', context)


@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('polls:home')

    if request.method == "POST":
        poll.delete()
        messages.success(request,
                         'Poll Deleted Successfully!!',
                         extra_tags='alert alert-danger alert-dismissable fade show')
        return redirect('polls:list')
    return render(request, 'polls/delete_poll.html', {'poll': poll})


@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('polls:home')
    if request.method == "POST":
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Poll Edit Successfull!!',
                             extra_tags='alert alert-success alert-dismissable fade show')
        return redirect('polls:list')
    else:
        form = EditPollForm(instance=poll)

    return render(request, 'polls/edit_poll.html', {'form': form, 'poll': poll})


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('polls:home')
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request,
                             'Your Choice Added Successfully!!',
                             extra_tags='alert alert-danger alert-dismissable fade show')
        return redirect('polls:list')
    else:
        form = ChoiceForm()
    return render(request, 'polls/add_choice.html', {'form': form})


@login_required
def edit_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('polls:home')

    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Choice Edited Successfully!!',
                             extra_tags='alert alert-primary alert-dismissable fade show')
        return redirect('polls:list')
    else:
        form = ChoiceForm(instance=choice)
    return render(request, 'polls/add_choice.html', {'form': form, 'edit_mode': True, 'choice': choice})


@login_required
def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('polls:home')

    if request.method == "POST":
        choice.delete()
        messages.success(request,
                         'Choice Deleted Successfully!!',
                         extra_tags='alert alert-danger alert-dismissable fade show')
        return redirect('polls:list')
    return render(request, 'polls/delete_choice.html', {'choice': choice})


@login_required
def poll_detail(request, poll_id):
    # polls = Poll.objects.get(id=poll_id)
    polls = get_object_or_404(Poll, id=poll_id)
    user_can_vote = polls.user_can_vote(request.user)
    results = polls.get_results_dict()
    context = {'polls': polls, 'user_can_vote': user_can_vote, 'results': results}
    return render(request, 'polls/polls_detail.html', context)
    # return HttpResponse(f"Your looking for polls with id:  {poll_id}")


def poll_vote(request, poll_id):
    polls = get_object_or_404(Poll, id=poll_id)
    if not polls.user_can_vote(request.user):
        messages.error(request, "Are you crazy? You already voted on this Poll!!")
        return HttpResponseRedirect(reverse('polls:detail', args=(poll_id,)))
    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=request.user, poll=polls, choice=choice)
        new_vote.save()
    else:
        messages.error(request, "Please choose one of the Field item..")
        return HttpResponseRedirect(reverse('polls:detail', args=(poll_id,)))
    return redirect('polls:detail', poll_id=poll_id)

# @login_required
# def your_polls(request):
#     polls = Poll.objects.filter(owner = request.user)
#     context = {
#         'polls':polls
#     }
#     return render(request, "polls/polls_list.html", context)
