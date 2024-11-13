from django import forms
from .models import User, Feedback, Review, Product, Cart, Wallet, Wishlist

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone
    
# class RatingForm(forms.Form):
#     RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
#     rating = forms.ChoiceField(choices=RATING_CHOICES, label='Оценка')

class CartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'text']

class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product']

class ReviewManager:
    @staticmethod
    def create_review(user, product, text, rating):
        return Review.objects.create(user=user, product=product, text=text, rating=rating)

    @staticmethod
    def get_product_reviews(product):
        return Review.objects.filter(product=product)

    @staticmethod
    def update_review(review, text, rating):
        review.text = text
        review.rating = rating
        review.save()

    @staticmethod
    def delete_review(review):
        review.delete()
