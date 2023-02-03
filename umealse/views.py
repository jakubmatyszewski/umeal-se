from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag

from .models import Event


def event_list(request: HttpRequest, tag_slug: str = '') -> HttpResponse:
    '''Generate view enlisting all published events.'''
    events = Event.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        print(tag)
        events = events.filter(tags__in=[tag])

    paginator = Paginator(events, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'umealse/event/list.html', {'events': events, 'tag': tag})


def event_detail(request: HttpRequest, id: int) -> HttpResponse:
    '''Generate detailed event view.'''
    event = get_object_or_404(Event,
                              id=id,
                              status=Event.Status.PUBLISHED)

    return render(request, 'umealse/event/detail.html', {'event': event})
