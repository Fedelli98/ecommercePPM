from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("research/", views.research, name="research"),
    path("details/<int:pk>/", views.details, name="details"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm),
         name='login'),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_cart/", views.updateCart, name="update_cart"),
    path("process_order/", views.processOrder, name="process_order"),
]
