from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("thank-you/", views.thank_you, name="thank_you"),
    path("booking/", views.booking, name="booking"),

    # Admin (owner)
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    # path("forgot-password/", views.forgot_password, name="forgot_password"),

    # ✅ Only dashboard now (owner_bookings removed)
    path("owner/dashboard/", views.owner_dashboard, name="owner_dashboard"),

    # Booking actions inside dashboard
    path("owner/bookings/view/<int:id>/", views.view_booking, name="view_booking"),
    path("owner/bookings/delete/<int:id>/", views.delete_booking, name="delete_booking"),
    path("owner/bookings/update-status/<int:id>/", views.update_status, name="update_status"),
    path("owner/bookings/export/", views.export_bookings_excel, name="export_bookings_excel"),

    # Gallery upload
    path("gallery-upload/", views.gallery_upload, name="gallery_upload"),
]
