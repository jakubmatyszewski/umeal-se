from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from taggit.models import Tag

from .forms import EventAddForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Event, Friendship, Profile


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
def add_event(request: HttpRequest) -> HttpResponse:
    """Create an event."""
    if request.method == "POST":
        add_event_form = EventAddForm(request.POST)
        if add_event_form.is_valid():
            new_event = add_event_form.save(commit=False)
            new_event.host_id = request.user.id
            new_event.slug = slugify(new_event.title)
            new_event.save()
            add_event_form.save_m2m()
            return redirect("event_detail", id=new_event.id)
    else:
        add_event_form = EventAddForm()

    return render(request, "event/add_event.html", {"add_event_form": add_event_form})


@login_required
def invite_to_event(request: HttpRequest, id: int) -> HttpResponse:
    ...


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request: HttpRequest) -> HttpResponse:
    """Create new user account."""
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request, "registration/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()

    return render(request, "registration/register.html", {"user_form": user_form})


@login_required
def show_profile(request: HttpRequest, username: str) -> HttpResponse:
    """Show user profile."""
    user = User.objects.get(username=username)
    return render(
        request,
        "account/profile.html",
        {"user": user},
    )


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


@login_required
def send_friend_request(request: HttpRequest, userID: int) -> HttpResponse:
    """Send a friend request to a user identified by userID."""
    from_user = request.user
    to_user = User.objects.get(id=userID)
    _, created = Friendship.objects.get_or_create(
        from_user=from_user.profile, to_user=to_user.profile
    )
    if created:
        messages.success(request, "Friend request sent.")
    else:
        messages.error(request, "Friend request was already sent.")

    return redirect("profile", username=to_user.username)


@login_required
def reject_friend_request(request: HttpRequest, requestID: int) -> HttpResponse:
    """Reject a friend request from another user.."""
    friend_request = Friendship.objects.get(id=requestID)
    if friend_request.to_user == request.user.profile:
        friend_request.delete()
        messages.success(request, "Friend request rejected.")
    else:
        messages.error(request, "Friend request can't be rejected.")
    return redirect("dashboard")


@login_required
def accept_friend_request(request: HttpRequest, requestID: int) -> HttpResponse:
    """Accept a friend request from another user.."""
    friend_request = Friendship.objects.get(id=requestID)
    if friend_request.to_user == request.user.profile:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.success(request, "Friend request accepted.")
    else:
        messages.error(request, "Friend request can't be accepted.")
    return redirect("dashboard")


@login_required
def delete_friend(request: HttpRequest, userID: int) -> HttpResponse:
    """Delete existing friendship."""
    user_profile = request.user.profile
    friend_profile = User.objects.get(id=userID).profile
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)

    return redirect("profile", username=friend_profile.user.username)
