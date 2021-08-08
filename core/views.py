from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages

from core.forms import RoomCreationForm, InviteForm, RespondToInviteForm
from core.models import Room
from core.mixins import PendingInviteMixin


class HomePageView(TemplateView):
    template_name = 'core/index.html'


# Rooms
class RoomListView(LoginRequiredMixin, PendingInviteMixin, ListView, FormView):
    template_name = 'core/room_list.html'
    model = Room
    context_object_name = 'rooms'
    form_class = RoomCreationForm
    success_url = reverse_lazy('room-list')

    def get_queryset(self):
        return self.request.user.rooms.all()

    def form_valid(self, form):
        name = form.cleaned_data['name']
        room = Room.objects.create(name=name)
        room.users.add(self.request.user)
        return super(RoomListView, self).form_valid(form)


class RoomDetailView(LoginRequiredMixin, DetailView):
    template_name = 'core/room_detail.html'
    context_object_name = 'room'

    def get_queryset(self):
        return self.request.user.rooms.all()


class InviteFormView(LoginRequiredMixin, FormView):
    template_name = 'core/room_invite.html'
    form_class = InviteForm

    def get_form_kwargs(self):
        k = super(InviteFormView, self).get_form_kwargs()
        k['room_id'] = self.kwargs['pk']
        return k

    def get_success_url(self):
        return reverse('room-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.send_invite(self.kwargs['pk'])
        return super(InviteFormView, self).form_valid(form)


@login_required
@require_POST
def respond_to_invite(request, pk):
    form = RespondToInviteForm(request.user, request.POST)
    if form.is_valid():
        form.handle_response()
        if form.cleaned_data['accept']:
            messages.add_message(request, messages.SUCCESS, 'successfully accepted invite')
            return redirect(reverse('room-detail', kwargs={'pk': pk}))
        else:
            messages.add_message(request, messages.SUCCESS, 'successfully declined invite')
            return redirect(reverse('room-list'))
    messages.add_message(request, messages.ERROR, f'{form.errors}')
    return redirect(reverse('room-list'))


class SocketTestView(TemplateView):
    template_name = 'core/ws_test.html'

    def get_context_data(self, **kwargs):
        ctx = super(SocketTestView, self).get_context_data(**kwargs)
        ctx['room_name'] = 'test_room'
        return ctx
