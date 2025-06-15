from django.urls import path
from .views import list_events, book_ticket, add_event

urlpatterns = [
    path('events/', list_events),
    path('book/',book_ticket),
    path('events/add/',add_event),
]