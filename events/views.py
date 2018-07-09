from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.utils import timezone

from .models import Event, Category
from .forms import EventForm, EventDeleteForm, SearchForm


class HomeView(TemplateView):
    """
    Standard generic template view
    """
    template_name = 'index.html'


def event_list(request, category_slug=None):
    """
    Queries the db for all categories and all events or 
    events of specific category depending on the url
    """
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        events = Event.objects.filter(category=category).select_related('host')
    else:
        events = Event.objects.all()

    return render(request,
                    'event_list.html',
                    {'category':category,
                        'categories':categories,
                        'events':events,})


def event_detail(request, event_slug):
    """
    Standard detail view
    """
    event = get_object_or_404(Event, slug=event_slug)
    return render(request, 'event_detail.html', {'event'})


@login_required
def my_events(request):
    """
    Queries the db for the current logged in
    user's events
    """
    events = Event.objects.filter(host=request.user)

    return render(request, 'my_events.html', {'events':events})



@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            return redirect('event_detail', slug=event.slug)
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form':form})


@login_required
def edit_event(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

    if event.host == request.user:
        if request.method == 'POST':
            form = EventForm(instance=event, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('event_detail', slug=event.slug)
        else:
            form = EventForm(instance=event)
        return render(request, 'event_form.html', {'form':form})
    else:
        raise PermissionDenied
    

@login_required
def delete_event(request, event_slug):
    """
    handles EventDelete form to make sure user
    wants to delete the event and authenticating his/her
    password as confirmation
    """
    event = get_object_or_404(Event, slug=event_slug)

    if event.host == request.user:
        if request.method=='POST':
            form = EventDeleteForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=event.user.username,
                                    password=cd['password'])
                if (user is not None) and (cd['title']==event.title):
                    event.delete()
                    messages.success(request,
                        'Your Event was deleted successfully!')
                    return redirect('my_events')
                else:
                    messages.error(request, 'Make sure you enter valid data.')
        else:
            form =  EventDeleteForm()
        return render(request, 'delete_event.html', {'form': form}) 

    else:
        raise PermissionDenied


def search(request):
    """
    Full text search and render the results
    """
    if request.method=='GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = Event.objects.annotate(
                    search=SearchVector('title',
                        'description',
                        'location',
                        'category__name'),).filter(search=cd['q'])
    return render(request, 'search.html', {'results':results})