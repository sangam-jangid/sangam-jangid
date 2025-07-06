from django.urls import path, include
from . import views
from django.conf.urls.static import static
from .views import OrderView

from django.conf import settings

urlpatterns = [
    path('', views.shop, name='shop'),
    path('biscuits/', views.biscuits, name='biscuit'),
    path('snacks/', views.snacks, name='snack'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('<str:username>/profile/', views.profile, name='profile'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('get_cart/', views.get_cart, name='get_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('order/', OrderView.as_view(), name='order'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('orders/<str:username>/', views.user_orders, name='user_orders'),
    path('take-order/<int:order_id>/', views.take_order, name='take_order'),
    path('chat/', views.chat_room, name='chat_room'),
    path('send/', views.send_message, name='send_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

