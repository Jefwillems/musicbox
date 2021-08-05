from django.contrib import admin
from core.models import Room, Invite


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass
