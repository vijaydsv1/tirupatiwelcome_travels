from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.urls import reverse
from urllib.parse import quote, urlencode
from functools import wraps
from datetime import datetime
import openpyxl

from django.conf import settings
from .forms import GalleryImageForm, BookingForm
from .models import GalleryImage, Booking
import os


# ✅ Admin Login Credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
OWNER_WHATSAPP = os.getenv("OWNER_WHATSAPP")



# ✅ Login Required Decorator
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("owner_logged_in"):
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)
    return wrapper


# ✅ ADMIN LOGIN
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session["owner_logged_in"] = True
            return redirect("owner_dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "travels/admin_login.html")


# ✅ ADMIN LOGOUT
def admin_logout(request):
    request.session.flush()
    return redirect("admin_login")


# ✅ GALLERY UPLOAD (protected)
@admin_required
def gallery_upload(request):
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect("gallery_upload")
    else:
        form = GalleryImageForm()

    images = GalleryImage.objects.all()
    return render(request, "travels/gallery_upload.html", {"form": form, "images": images})


# ✅ PUBLIC PAGES
def index(request):
    images = GalleryImage.objects.all()
    return render(request, "travels/index.html", {"images": images})

def about(request):
    return render(request, "travels/about.html")

def services(request):
    return render(request, "travels/services.html")

def booking(request):
    return render(request, "travels/booking.html")


# ✅ CONTACT PAGE WITH BOOKING FORM
def contact(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # ✅ WhatsApp message
            whatsapp_message = (
                f"New Booking Received ✅\n\n"
                f"Name: {booking.full_name}\n"
                f"Phone: {booking.phone}\n"
                f"Service: {booking.service}\n"
                f"Pickup: {booking.pickup}\n"
                f"Drop: {booking.drop}\n"
                f"Message: {booking.message or '-'}"
            )

            wa_url = f"https://wa.me/{OWNER_WHATSAPP}?text={quote(whatsapp_message)}"

            # ✅ Email to admin
            email_subject = f"New Booking from {booking.full_name}"
            email_body = (
                f"Name: {booking.full_name}\n"
                f"Email: {booking.email or '-'}\n"
                f"Phone: {booking.phone}\n"
                f"Service: {booking.service}\n"
                f"Pickup: {booking.pickup}\n"
                f"Drop: {booking.drop}\n"
                f"Message: {booking.message or '-'}\n"
            )

            send_mail(
                email_subject,
                email_body,
                "noreply@tirupatiwelcometravels.com",
                ["info@tirupatiwelcometravels.com"],
                fail_silently=True,
            )

            return redirect(f"/thank-you/?wa={quote(wa_url)}")

    else:
        form = BookingForm()

    return render(request, "travels/contact.html", {"form": form})


# ✅ THANK YOU PAGE
def thank_you(request):
    wa_url = request.GET.get("wa")
    return render(request, "travels/thank_you.html", {"wa_url": wa_url})


# ✅ OWNER DASHBOARD
@admin_required
def owner_dashboard(request):
    bookings = Booking.objects.order_by("-created_at")

    search = request.GET.get("search", "")
    service = request.GET.get("service", "")
    date = request.GET.get("date", "")

    if search:
        bookings = bookings.filter(full_name__icontains=search)

    if service:
        bookings = bookings.filter(service=service)

    if date:
        bookings = bookings.filter(created_at__date=date)

    today = datetime.now().date()

    context = {
        "bookings": bookings,
        "search": search,
        "service": service,
        "date": date,
        "total_bookings": Booking.objects.count(),
        "today_bookings": Booking.objects.filter(created_at__date=today).count(),
        "outstation_count": Booking.objects.filter(service="Outstation Trip").count(),
    }

    return render(request, "travels/owner_dashboard.html", context)


# ✅ VIEW BOOKING IN POPUP
@admin_required
def view_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    return render(request, "travels/view_booking_modal.html", {"booking": booking})


# ✅ DELETE BOOKING
def delete_booking(request, id):
    if not request.session.get("owner_logged_in"):
        return redirect("admin_login")

    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return redirect("owner_dashboard")

# ✅ UPDATE STATUS
@admin_required
def update_status(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        booking.status = new_status
        booking.save()
        return redirect("owner_dashboard")

    return render(request, "travels/edit_status_modal.html", {"booking": booking})


# ✅ DOWNLOAD EXCEL
@admin_required
def export_bookings_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Bookings"

    headers = ["Name", "Email", "Phone", "Service", "Pickup", "Drop", "Message", "Status", "Date"]
    sheet.append(headers)

    for b in Booking.objects.all():
        sheet.append([
            b.full_name,
            b.email,
            b.phone,
            b.service,
            b.pickup,
            b.drop,
            b.message,
            b.status,
            b.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = f'attachment; filename="bookings_{datetime.now().strftime("%Y%m%d")}.xlsx"'

    workbook.save(response)
    return response
