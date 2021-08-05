from django.urls import path
from core.views import HomePageView, RoomListView, RoomDetailView, InviteFormView, respond_to_invite

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/invite/', InviteFormView.as_view(), name='room-invite'),
    path('rooms/<int:pk>/invite/respond/', respond_to_invite, name='room-invite-response'),
    path('', HomePageView.as_view(), name='index'),
]
