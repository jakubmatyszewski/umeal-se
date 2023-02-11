from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from taggit.models import Tag

from .forms import UserRegistrationForm
from .models import Event


@login_required
def event_list(request: HttpRequest, tag_slug: str = '') -> HttpResponse:
    '''Generate view enlisting all published events.'''
    events = Event.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        events = events.filter(tags__in=[tag])

    paginator = Paginator(events, 10)
    page_number = request.GET.get('page', 1)

    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'umealse/event/list.html', {'events': events, 'tag': tag, 'section': 'events'})


@login_required
def event_detail(request: HttpRequest, id: int) -> HttpResponse:
    '''Generate detailed event view.'''
    event = get_object_or_404(Event,
                              id=id,
                              status=Event.Status.PUBLISHED)

    return render(request, 'umealse/event/detail.html', {'event': event, 'section': 'events'})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'umealse/account/dashboard.html', {'section': 'dashboard'})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {'user_form': user_form})
