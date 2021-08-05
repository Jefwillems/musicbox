from django.views.generic.base import ContextMixin
from core.models import Invite


class PendingInviteMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(PendingInviteMixin, self).get_context_data(**kwargs)
        context['pending_invites'] = Invite.objects.filter(user=self.request.user)
        return context
