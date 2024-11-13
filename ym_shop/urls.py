from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('catalog/', views.catalog, name='catalog'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('items/<str:category>/', views.item_list, name='item_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('order/', views.order_view, name='order'),
    path('saved-items/', views.saved_items_view, name='saved_items'),
    path('guide/', views.guide_view, name='guide'),
    #path('rating/', views.rating_view, name='rating'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]