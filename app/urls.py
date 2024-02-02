from django.urls import path
from src.core.views import home, mail, chat, auth, contact, profile, setting, admin
from src.core.views import user, category, product, order, article, coupon
from src.core.api import route

urlpatterns = [
    path('', home.index),
    path('mail', mail.index),
    path('chat', chat.index),
    path('login', auth.login),
    path('lock-screen', auth.lockscreen),
    path('logout', auth.logout),
    path('lockout', auth.lockout),
    path('profile', profile.index),
    path('settings', setting.index),
    path('contacts', contact.index),
    path('coupons', coupon.index),
    path('add-coupon', coupon.add),
    path('admins', admin.index),
    path('add-admin', admin.add),
    path('edit-admin/<id>', admin.edit),
    path('users', user.index),
    path('add-user', user.add),
    path('edit-user/<id>', user.edit),
    path('categories', category.index),
    path('add-category', category.add),
    path('edit-category/<id>', category.edit),
    path('products', product.index),
    path('add-product', product.add),
    path('edit-product/<id>', product.edit),
    path('orders', order.index),
    path('add-order', order.add),
    path('edit-order/<id>', order.edit),
    path('articles', article.index),
    path('add-article', article.add),
    path('edit-article/<id>', article.edit),
] + route.routes
