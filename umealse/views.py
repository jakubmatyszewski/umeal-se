from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from .models import Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def event_list(request: HttpRequest) -> HttpResponse:
    '''Generate view enlisting all published events.'''
    events = Event.published.all()
    paginator = Paginator(event_list, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'umealse/event/list.html', {'events': events})


def event_detail(request: HttpRequest, id: int) -> HttpResponse:
    '''Generate detailed event view.'''
    event = get_object_or_404(Event,
                              id=id,
                              status=Event.Status.PUBLISHED)

    return render(request, 'umealse/event/detail.html', {'event': event})
