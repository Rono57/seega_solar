
from django.shortcuts import render,HttpResponse

from app.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.http import JsonResponse

from django.db.models import Q


import logging



from datetime import *

# Create your views here.


def home(request):
    return render(request, 'home.html')



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


def stf_task(request):
    a=Task.objects.filter(staff_id=request.session['sid'])
    return render(request, 'stf_task.html',{'tasks':a})

from django.shortcuts import render
from .models import Task

def st_pack(request,id):
   
    tasks = Task.objects.filter(order_id=id).select_related('order__package').prefetch_related('materials_used')

    return render(request, 'stf_pack.html', {'packages': tasks})



from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Task, Item

def st_used(request, id):
    task = get_object_or_404(Task, id=id)  # Get the task
    all_items = Item.objects.all()  # Fetch all available items
    used_items = task.materials_used.all()  # Fetch materials already used for the task

    if request.method == "POST":
        item_id = request.POST.get("item")  # Get selected item ID from form
        if item_id:
            item = get_object_or_404(Item, id=item_id)
            task.materials_used.add(item)  # Add the item to the task
            task.save()
            return redirect('st_used', id=id)  # Refresh page after adding

    return render(request, "st_used.html", {"a": all_items, "b": used_items, "task": task})



def admin_review(request):
    a=Review.objects.all()
    return render(request, 'adm_review.html',{'reviews':a})



def sbooking(request):
    a=Sbook.objects.all()
    return render(request, 'view_sbook.html',{'a':a})


def user_view_ser(request):
    a=Services.objects.all()
    return render(request, 'user_view_ser.html',{'a':a})

def user_view_sbook(request):
    a=Sbook.objects.filter(user_id=request.session['uid'])
    return render(request, 'user_view_sbook.html',{'a':a})


def user_view_assigned_sbook(request,id):
    a=Assign_sbook.objects.filter(sbook_id=id)
    return render(request, 'user_view_assigned_sbook.html',{'a':a})


def book_ser(request,id):
    a=Sbook(user_id=request.session['uid'],service_id=id,date=datetime.now(),status='Pending')
    a.save()
    return HttpResponse("<script>alert('Service Booked Successfully');window.location='/user_view_sbook';</script>")



def assign_sbook(request,id):
    c=Staff.objects.all()
    
    if request.method == 'POST':
        sid = request.POST['sid']
        a=Assign_sbook(staff_id=sid,sbook_id=id,adate=datetime.now(),)
        a.save()
        return HttpResponse("<script>alert('Assigned');window.location='/sbooking';</script>")
    z=Assign_sbook.objects.filter(sbook_id=id)
    return render(request, 'adm_assign_sbook.html',{'a':c,'z':z})

    



def assign_worker(request, id):
    try:
        v = Task.objects.get(order_id=id)  # Try to fetch existing task
    except Task.DoesNotExist:
        v = None  # No task exists, allow user to create a new one

    z = Staff.objects.all()  # Fetch all staff members

    if request.method == 'POST':
        wid = request.POST['wid']
        print(wid,"////////")
        
        if v:  # If task exists, update it
            v.staff_id = wid
            v.updated_at = datetime.now()
            v.status = 'pending'
            v.save()
        else:  # If no task exists, create a new one
            v = Task(staff_id=wid, order_id=id, updated_at=datetime.now(), status='pending')
            v.save()

        return HttpResponse("<script>alert('Worker Assigned Successfully');window.location='/adm_order';</script>")

    return render(request, 'assigne_worker.html', {'z': z, 'v': v})

def user_package(request):
    packages = Package.objects.all()
    items = Item.objects.all()
    return render(request, 'user_package.html', {'packages': packages, 'items': items})
   
  


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Staff, Login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

def manage_staff(request):
    if request.method == "POST":
        # Form handling to create a new staff
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        position = request.POST.get('position')
        username = request.POST.get('uname')
        password = request.POST.get('password')

        # Create a login instance for the staff
        login = Login.objects.create(
            username=username,
            password=make_password(password),  # Hashing the password for security
            usertype="staff"
        )

        # Create the staff instance and associate it with the login
        staff = Staff.objects.create(
            login=login,
            name=name,
            email=email,
            phone=phone,
            position=position
        )

        # Redirect with a success message
        messages.success(request, 'Staff added successfully!')
        return redirect('manage_staff')  # Adjust the redirect URL as needed

    # Render staff list and the form for adding new staff
    staffs = Staff.objects.all()
    return render(request, 'manage_staff.html', {'staffs': staffs})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Services  # Assuming Services is your model

def manage_services(request):
    if request.method == "POST":
        if 'submit' in request.POST:
            # Form handling to create a new service
            sname = request.POST.get('sname')
            des = request.POST.get('des')

            # Create the service instance
            ser = Services.objects.create(
                sname=sname,
                description=des,
            )

            # Redirect with a success message
            messages.success(request, 'Service added successfully!')
            return redirect('manage_services')

        elif 'delete' in request.POST:
            # Handle service deletion
            delete_id = request.POST.get('delete_id')
            try:
                service = Services.objects.get(id=delete_id)
                service.delete()
                messages.success(request, 'Service deleted successfully!')
            except Services.DoesNotExist:
                messages.error(request, 'Service not found!')
            return redirect('manage_services')

    # Render service list and the form for adding new services
    staffs = Services.objects.all()
    return render(request, 'manage_services.html', {'a': staffs})


from django.shortcuts import render, redirect
from .models import Vendor, Login
from django.contrib.auth.hashers import make_password

def manage_vendor(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
 

        

        # Create a Vendor object
        vendor = Vendor(
   
            name=name,
            email=email,
            contact=phone,
            address=address
        )
        vendor.save()

        return redirect('manage_vendor')  # Redirect to the same page to refresh the vendor list

    # Retrieve all vendors from the database to display them
    vendors = Vendor.objects.all()
    return render(request, 'manage_vendor.html', {'vendors': vendors})



from django.shortcuts import render, redirect
from .models import Item, Vendor
from django.contrib import messages

def manage_item(request):
    # If the form is submitted
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        price = request.POST['price']
        quantity = request.POST['quantity']
        vendor_id = request.POST['vendor']
        vendor = Vendor.objects.get(id=vendor_id)
        
        # Create the new item
        item = Item.objects.create(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            vendor=vendor
        )
        messages.success(request, 'Item added successfully!')
        return redirect('manage_item')  # Redirect to refresh the page and show updated list

    # Fetch all items and vendors to display on the form
    items = Item.objects.all()
    vendors = Vendor.objects.all()
    return render(request, 'manage_item.html', {'items': items, 'vendors': vendors})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Vendor
from django.contrib import messages

def edit_item(request, item_id):
    # Get the item object and all vendors
    item = get_object_or_404(Item, id=item_id)
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        # Update the item details
        item.name = request.POST['name']
        item.category = request.POST['category']
        item.price = request.POST['price']
        item.quantity = request.POST['quantity']
        
        # Get the selected vendor
        vendor_id = request.POST['vendor']
        vendor = Vendor.objects.get(id=vendor_id)
        item.vendor = vendor
        
        # Save the updated item
        item.save()

        messages.success(request, 'Item updated successfully!')
        return redirect('manage_item')  # Redirect back to the manage items page

    return render(request, 'edit_item.html', {'item': item, 'vendors': vendors})

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('manage_item')


from django.shortcuts import render, redirect
from .models import Package, Item
from django.http import HttpResponse

def manage_package(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        items_ids = request.POST.getlist('items')  # Get the selected items

        # Create a new package
        package = Package.objects.create(
            name=name, 
            description=description, 
            price=price
        )
        
        # Add items to the package
        for item_id in items_ids:
            item = Item.objects.get(id=item_id)
            package.items.add(item)

        return redirect('manage_package')  # Redirect back to the manage_package page
    
    items = Item.objects.all()
    packages = Package.objects.all()
    return render(request, 'manage_packages.html', {'items': items, 'packages': packages})


from django.shortcuts import get_object_or_404, render, redirect
from .models import Package, Item

def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        # Update the package details
        package.name = request.POST.get('name')
        package.description = request.POST.get('description')
        package.price = request.POST.get('price')

        # Update the items associated with the package
        items_ids = request.POST.getlist('items')  # Get the selected items
        package.items.clear()  # Remove all existing items before adding new ones
        for item_id in items_ids:
            item = Item.objects.get(id=item_id)
            package.items.add(item)

        package.save()
        return redirect('manage_package')  # Redirect to manage packages page after edit

    items = Item.objects.all()
    return render(request, 'edit_package.html', {'package': package, 'items': items})


from django.shortcuts import get_object_or_404, redirect
from .models import Package

def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    package.delete()  # Delete the package
    return redirect('manage_package')  # Redirect to manage packages page after delete











def reply(request,id):
    a=Complaint.objects.get(pk=id)
 
    if request.method=='POST':
        rep=request.POST['rep']
        
        a.reply=rep
        a.save()
        return HttpResponse("<script>alert('Replied Successfully');window.location='/adm_com';</script>")
    return render(request,'reply.html')



def adm_com(request):
    a=Complaint.objects.filter(reply='pending')
    return render(request,'adm_com.html',{'a':a})


from django.contrib.auth import authenticate, login as django_login
from django.http import HttpResponse
from django.shortcuts import render
from .models import Login, Staff, User



def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        psw = request.POST['psw']
        
        print(uname, psw)
        
        try:
            # Fetch user from Login model
            lg = Login.objects.get(username=uname)
            
            # If user is admin, login as usual without password hashing
            if lg.usertype == 'admin':
                if lg.password == psw:  # Admin login uses direct password match
                    print(lg, "///////////////")
                    request.session['login_id'] = lg.pk
                    return HttpResponse("<script>alert('Login Successfully');window.location='/adm';</script>")
                else:
                    return HttpResponse("<script>alert('Invalid admin password...');window.location='/login';</script>")
            
            # If user is staff or user, use Django's password-checking mechanism
            if lg.usertype in ['staff', 'user']:
                # Use Django's password checking for staff and user
                if lg.check_password(psw):  # Check hashed password
                    print(lg, "///////////////")
                    request.session['login_id'] = lg.pk
                    lid = request.session['login_id']
                    
                    # Redirect based on user type
                    if lg.usertype == 'staff':
                        staff = Staff.objects.get(login_id=lid)
                        if staff:
                            request.session['sid'] = staff.pk
                            return HttpResponse("<script>alert('Login Successfully');window.location='/staff';</script>")
                    
                    elif lg.usertype == 'user':
                        user = User.objects.get(login_id=lid)
                        if user:
                            request.session['uid'] = user.pk
                            return HttpResponse("<script>alert('Login Successfully');window.location='/user';</script>")
                else:
                    return HttpResponse("<script>alert('Invalid credentials...');window.location='/login';</script>")
            
        except Login.DoesNotExist:
            return HttpResponse("<script>alert('User does not exist...');window.location='/login';</script>")
        except Exception as e:
            print(e)
            return HttpResponse("<script>alert('Login Failed...!!!!');window.location='/login';</script>")

    return render(request, 'login.html')



def adm(request):
    return render(request,'admin.html')


def send_request(request,id):
    z=Order(package_id=id,estimate_price=0,confirmed=False,payment_status=False,created_at=datetime.now(),user_id=request.session['uid'])
    z.save()
    return HttpResponse("<script>alert('Request Sent Successfully');window.location='/user_order';</script>")
   

def send_estimate(request,id):
    z=Order.objects.get(pk=id)
    if request.method=='POST':
        est=request.POST['amount']
        z.estimate_price=est
        z.save()
       
       
        return HttpResponse("<script>alert('Estimate Sent Successfully');window.location='/user_order';</script>")
    return render(request,'send_estimate.html')


def make_payment(request,id):
    z=Order.objects.get(pk=id)
    am=z.estimate_price
    if request.method=='POST':
        z.payment_status=True
        z.save()
       
       
        return HttpResponse("<script>alert('Estimate Sent Successfully');window.location='/user_order';</script>")
    return render(request,'make_payment.html',{'am':am})

def reject_order(request,id):
    z=Order.objects.get(pk=id)
    z.payment_status=False
    z.estimate_price=0
    z.save()
    return HttpResponse("<script>alert('Order Rejected Successfully');window.location='/adm_order';</script>")

def approve_order(request,id):
    z=Order.objects.get(pk=id)
    
    z.confirmed=1
    z.save()
    return HttpResponse("<script>alert('Order Approved Successfully');window.location='/adm_order';</script>")


def up_com(request,id):
    z=Task.objects.get(pk=id)
    
    z.status='completed'
    z.save()
    return HttpResponse("<script>alert('Task Completed Successfully');window.location='/staff';</script>")

def remove(request,id):
    z=Order.objects.get(pk=id)
    
    
    z.delete()
    return HttpResponse("<script>alert('Removed Successfully');window.location='/user_order';</script>")







def user_complaint(request):
    z=Complaint.objects.filter(user_id=request.session['uid'])
    if request.method=='POST':
        comp=request.POST['comp']
        Complaint.objects.create(user_id=request.session['uid'],message=comp,reply='pending',created_at=datetime.now())
        
        return HttpResponse("<script>alert('Complaint Sent Successfully');window.location='/user_complaint';</script>")
    return render(request,'user_complaint.html',{'z':z})


def user_reviews(request):
    if request.method=='POST':
        rating=request.POST['rating']
        comment=request.POST['comment']
        Review.objects.create(user_id=request.session['uid'],rating=rating,comment=comment,created_at=datetime.now())
        
        return HttpResponse("<script>alert('Review Sent Successfully');window.location='/user_reviews';</script>")
    return render(request,'user_review.html')


def user_order(request):
    a=Order.objects.filter(user_id=request.session['uid'])
    items = Item.objects.all()
    
    
    return render(request,'user_order.html',{'a':a,'items':items})


def adm_order(request):
    a=Order.objects.all()
    items = Item.objects.all()
    
    
    return render(request,'adm_order.html',{'a':a,'items':items})



from django.shortcuts import render
from .models import User, Login
from django.shortcuts import render, redirect
from .models import User, Login

def user_profile(request):
    if 'login_id' in request.session:
        try:
            login_instance = Login.objects.get(id=request.session['login_id'])
            user = User.objects.get(login=login_instance)  # Fetch user details
            return render(request, 'user_profile.html', {'user': user})
        except User.DoesNotExist:
            return render(request, 'user_profile.html', {'error': 'User profile not found'})
    else:
        return render(request, 'user_profile.html', {'error': 'User not logged in'})

def edit_user_profile(request):
    if 'login_id' in request.session:
        try:
            login_instance = Login.objects.get(id=request.session['login_id'])
            user = User.objects.get(login=login_instance)

            if request.method == "POST":
                user.name = request.POST['name']
                user.email = request.POST['email']
                user.phone = request.POST['phone']
                user.address = request.POST['address']
                user.save()
                return redirect('user_profile')  # Redirect to the profile page after update

            return render(request, 'edit_user_profile.html', {'user': user})

        except User.DoesNotExist:
            return redirect('user_profile')  # Redirect back if user doesn't exist
    else:
        return redirect('user_profile')  # Redirect if not logged in


def staff(request):
    return render(request,'staff.html')

def user(request):
    return render(request,'user.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login, User
from django.contrib.auth.hashers import make_password

def user_reg(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("user_reg")

        # Check if username already exists
        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("user_reg")

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("user_reg")

        # Create login entry
        login_entry = Login.objects.create(username=username, password=make_password(password), usertype="user")

        # Create user entry linked to login
        User.objects.create(
            login=login_entry,
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("user_reg")  # Redirect to login page

    return render(request, "user_reg.html")

