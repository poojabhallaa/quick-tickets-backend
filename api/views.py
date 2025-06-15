
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .firestore import db

@api_view(['GET'])
def list_events(request):
    events = db.collection('events').stream()
    data = [doc.to_dict() | {'id': doc.id} for doc in events]
    return Response(data)

@api_view(['POST'])
def book_ticket(request):
    data = request.data
    event_id = data.get('event_id')
    name = data.get('name')
    email = data.get('email')
    seats = int(data.get('seats', 1))

    # Get event
    event_ref = db.collection('events').document(event_id)
    event_doc = event_ref.get()

    if not event_doc.exists:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    event_data = event_doc.to_dict()
    available_seats = event_data.get('available_seats', 0)

    if seats > available_seats:
        return Response({'error': 'Not enough seats available'}, status=status.HTTP_400_BAD_REQUEST)

    # Save booking
    db.collection('bookings').add({
        'event_id': event_id,
        'name': name,
        'email': email,
        'seats': seats
    })

    # Update event seat count
    event_ref.update({
        'available_seats': available_seats - seats
    })

    return Response({'success': True})


@api_view(['POST'])
def add_event(request):
    data = request.data
    name = data.get('name')
    location = data.get('location')
    date = data.get('date')
    available_seats = int(data.get('available_seats', 0))

    if not all([name, location, date]):
        return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

    new_event = {
        'name': name,
        'location': location,
        'date': date,
        'available_seats': available_seats,
    }

    event_ref = db.collection('events').add(new_event)
    event_id = event_ref[1].id

    return Response({'success': True, 'id': event_id}, status=201)



