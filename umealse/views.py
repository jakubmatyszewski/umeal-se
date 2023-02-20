from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from taggit.models import Tag

from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Event, Profile, Friendship


def landing_page(request: HttpRequest) -> HttpResponse:
    """Root page seen by all (registered or not) users."""
    return render(request, "landing_page.html")


@login_required
def event_list(request: HttpRequest, tag_slug: str = "") -> HttpResponse:
    """Generate view enlisting all published events."""
    events = Event.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        events = events.filter(tags__in=[tag])

    paginator = Paginator(events, 10)
    page_number = request.GET.get("page", 1)

    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(
        request,
        "event/list.html",
        {"events": events, "tag": tag, "section": "events"},
    )


@login_required
def event_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Generate detailed event view."""
    event = get_object_or_404(Event, id=id, status=Event.Status.PUBLISHED)

    return render(request, "event/detail.html", {"event": event, "section": "events"})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request: HttpRequest) -> HttpResponse:
    """Create new user account."""
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    """Enable user to edit their profile."""
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "Error updating your profile.")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "account/edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
