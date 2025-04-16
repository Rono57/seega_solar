
import logging
from django.shortcuts import render
from django.db.models import Q
from .models import ChatMessage

logger = logging.getLogger("django")

def chat_with_admin(request):
    logger.debug("📢 chat_with_admin() view called.")  # Logging start

    staff_id = request.session.get("login_id")  # Get logged-in user ID
    admin_id = 1  # Admin ID is fixed as 1

    if not staff_id:
        logger.error("❌ Staff login ID not found in session.")
        return render(request, "error.html", {"message": "You must be logged in."})

    # Fetch chat messages using Q object
    messages = ChatMessage.objects.filter(
        Q(sender_id=staff_id, receiver_id=admin_id) | Q(sender_id=admin_id, receiver_id=staff_id)
    ).order_by("timestamp")

    logger.info(f"📩 Fetched {messages.count()} messages.")  # Log message count

    for msg in messages:
        logger.debug(f"🔹 {msg.timestamp} | {msg.sender_id} -> {msg.receiver_id} : {msg.message}")
    
    print(messages)

    return render(request, "chat_with_admin.html", {"messages": messages})


def send_message(request):
    if request.method == "POST":
        sender_id = request.session.get('login_id')
        receiver_id = request.POST.get('receiver_id')
        message_text = request.POST.get('message')

        if sender_id and receiver_id and message_text:
            ChatMessage.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message_text
            )
            return JsonResponse({"success": True})

    return JsonResponse({"success": False})



import logging
from django.shortcuts import render
from django.db.models import Q
from .models import ChatMessage

logger = logging.getLogger("django")

logger = logging.getLogger(__name__)

def chat_with_staff(request, id):
    """
    Chat view for admin to chat with a particular staff member.
    'id' is the staff login id passed as URL parameter.
    """
    logger.debug("📢 chat_with_staff() view called.")

    admin_id = 1  # Admin ID is fixed
    staff_id = id  # Use the passed argument as staff id

    if not staff_id:
        logger.error("❌ Staff login ID not provided as argument.")
        return render(request, "error.html", {"message": "Staff login id is missing."})

    # Fetch messages between admin and the given staff using Q objects
    messages = ChatMessage.objects.filter(
        Q(sender_id=admin_id, receiver_id=staff_id) | Q(sender_id=staff_id, receiver_id=admin_id)
    ).order_by("timestamp")

    logger.info(f"📩 Fetched {messages.count()} messages for staff {staff_id}.")
    for msg in messages:
        logger.debug(f"🔹 {msg.timestamp} | {msg.sender_id} -> {msg.receiver_id} : {msg.message}")

    # Pass the staff id to the template so it can be used in the message form
    return render(request, "chat_with_staff.html", {"messages": messages, "staff_id": staff_id})



def send_message_staff(request):
    """
    Handles sending a message from the admin to a staff member.
    Assumes the admin is logged in and their login id is stored in the session.
    """
    if request.method == "POST":
        data = request.POST
        # For admin chat, we use the session login id as sender.
        sender_id = request.session.get("login_id")
        receiver_id = data.get("receiver_id")
        message_text = data.get("message")

        if sender_id and receiver_id and message_text:
            ChatMessage.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message_text
            )
            return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"})



      path("chat_with_staff/<int:id>/", views.chat_with_staff, name="chat_with_staff"),
    path("send_message_staff/", views.send_message_staff, name="send_message_staff"),
    path('send_message/', views.send_message, name='send_message'),
    