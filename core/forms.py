from django import forms
from core.models import Room, Invite
from django.contrib.auth import get_user_model
from django.db.models import Q


def get_user(email):
    return get_user_model().objects.filter(email=email).first()


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', ]


class InviteForm(forms.ModelForm):
    user = forms.EmailField()

    def __init__(self, room_id, **kwargs):
        super(InviteForm, self).__init__(**kwargs)
        self.room_id = room_id

    def clean_user(self):
        us = get_user(self.cleaned_data['user'])
        if not us:
            raise forms.ValidationError(message='Invited user does not exist.')
        if Room.objects.filter(pk=self.room_id, sent_invites__user_id=us.pk).exists():
            raise forms.ValidationError(message='This user already has an invite.')
        if Room.objects.filter(pk=self.room_id, users__in=[us]).exists():
            raise forms.ValidationError(message='This user is already in the group.')
        return us

    def send_invite(self, room_id):
        message = self.cleaned_data['message']
        user = self.cleaned_data['user']
        return Invite.objects.create(message=message,
                                     room_id=room_id,
                                     user=get_user_model().objects.get(email=user))

    class Meta:
        model = Invite
        fields = ['message', 'user']


class RespondToInviteForm(forms.Form):
    accept = forms.BooleanField(required=True)
    invite_id = forms.IntegerField()

    def __init__(self, user, *args, **kwargs):
        super(RespondToInviteForm, self).__init__(*args, **kwargs)
        self.for_user = user

    def clean_invite_id(self):
        inv = Invite.objects.filter(pk=self.cleaned_data['invite_id'], user=self.for_user)
        if not inv.exists():
            raise forms.ValidationError('The specified invite does no longer exist.')
        return inv.first()

    def handle_response(self):
        inv = self.cleaned_data['invite_id']
        inv.room.users.add(self.for_user)
        inv.delete()
        return inv
