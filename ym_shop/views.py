# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import RegistrationForm, CartForm, FeedbackForm, ReviewUpdateForm, WishlistForm
from .models import Product, User, Cart, Wallet, Review, Feedback, Wishlist, Order, OrderItem

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def welcome(request): 
    return render(request, 'welcome.html') 

def catalog(request):
    products_list = Product.objects.filter(is_active=True)
    paginator = Paginator(products_list, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'catalog.html', {'products': products})

def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def add_to_wishlist(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        Wishlist.objects.get_or_create(user=request.user, product=product)
        return redirect('wishlist')

def remove_from_wishlist(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    wishlist_item.delete()
    return redirect('wishlist')

def item_list(request, category): 
    products = Product.objects.filter(category=category) 
    paginator = Paginator(products, 10) 
    page_number = request.GET.get('page') 
    products_page = paginator.get_page(page_number) 
    return render(request, 'item_list.html', {'products': products_page, 'category': category}) 

def add_to_cart(request, product_id): 
    if request.method == "POST": 
        product = get_object_or_404(Product, id=product_id) 
        quantity = request.POST.get('quantity', 1) 
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product) 
        cart_item.quantity += int(quantity) 
        cart_item.save() 
        return redirect('catalog') 

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def order_view(request):
    if request.method == "POST":
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.exists():
            order = Order.objects.create(user=request.user, total_price=sum(item.product.price * item.quantity for item in cart_items))
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            cart_items.delete()
            return redirect('order_success')
    return render(request, 'order.html')

def wallet_view(request): 
    user_wallet = get_object_or_404(Wallet, user=request.user) 
    return render(request, 'wallet.html', {'wallet': user_wallet}) 

def saved_items_view(request): 
    saved_items = []  
    total_price = sum(item.price for item in saved_items) 
    return render(request, 'saved_items.html', {'saved_items': saved_items, 'total_price': total_price}) 

def guide_view(request): 
    return render(request, 'guide.html') 

# def rating_view(request): 
#     if request.method == "POST": 
#         form = RatingForm(request.POST) 
#         if form.is_valid(): 
#             Review.objects.create(user=request.user, rating=int(form.cleaned_data['rating']))
#             reviews = Review.objects.all() 
#             return render(request, 'rating.html', {'reviews': reviews}) 
#     reviews = Review.objects.all()  
#     return render(request, 'rating.html', {'reviews': reviews})

def feedback_view(request): 
    if request.method == "POST": 
        form = FeedbackForm(request.POST) 
        if form.is_valid(): 
            Feedback.objects.create(user=request.user, subject=form.cleaned_data['subject'], text=form.cleaned_data['text']) 
            return redirect('feedback')  
    else:  
        form = FeedbackForm() 
    return render(request, 'feedback.html', {'form': form}) 

def edit_review(request, review_id): 
    review = get_object_or_404(Review, id=review_id, user=request.user) 
    if request.method == "POST": 
        form = ReviewUpdateForm(request.POST, instance=review) 
        if form.is_valid(): 
            form.save() 
            return redirect('rating') 
    else:  
        form = ReviewUpdateForm(instance=review) 
    return render(request, 'edit_review.html', {'form': form}) 

def delete_review(request, review_id): 
    review = get_object_or_404(Review, id=review_id, user=request.user) 
    review.delete() 
    return redirect('rating')