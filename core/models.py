from django.db import models
from django.contrib.auth import get_user_model


class Room(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name='rooms', blank=True)

    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Invite(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='invites', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='sent_invites', on_delete=models.CASCADE)

    message = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.room} -> {self.user}'
