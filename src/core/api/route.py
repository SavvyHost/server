from django.urls import path
from src.core.api import account, auth, booking, chat, product

routes = [
    path('api/all-data', product.all_data),
    path('api/register', auth.register),
    path('api/login', auth.login),
    path('api/recovery', auth.recovery),
    path('api/change-password', auth.change_password),
    path('api/check-token', auth.check_token),
    path('api/destination', product.destination_data),
    path('api/tour', product.tour_data),
    path('api/search', product.search_tours),
    path('api/bookings', booking.bookings_data),
    path('api/change-status', booking.change_status),
    path('api/remove-booking', booking.remove_booking),
    path('api/wishlist', product.wishlist_data),
    path('api/discount', booking.discount),
    path('api/paid-booking', booking.paid_booking),
    path('api/later-booking', booking.later_booking),
    path('api/account', account.info),
    path('api/edit-account', account.edit),
    path('api/reset-password', account.reset_password),
    path('api/send-message', chat.send),
    path('api/active-messages', chat.active),
    path('api/get-messages', chat.messages),
]
