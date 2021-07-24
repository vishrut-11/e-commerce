from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import Loginform, Mypasswordchangeform, MypasswordResetform, Mysetpasswordform

urlpatterns = [
    # path('', views.home),
    path("", views.ProductView.as_view(), name="home"),
#ProductDetail    
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
#add-to-cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
#show_cart
    path("cart/", views.show_cart, name="showcart"),
#Plus(item)
    path("pluscart/", views.plus_cart),

    path("minuscart/", views.minus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),    
    
#profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
#profile_update
    path('<int:id>', views.update_data, name="updatedata"),
#profile_delete
    path('delete/<int:id>', views.delete_data, name="deletedata"),
#address
    path('address/', views.address, name='address'),

#Topwear   
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
#Bottomwear
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
#mobile
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
#Laptop
    path("laptop/", views.laptop, name="laptop"),
    path("laptop/<slug:data>", views.laptop, name="laptopdata"),
#login
    path('accounts/login/', auth_views.LoginView.as_view(template_name="app/login.html", authentication_form=Loginform), name='login'),

#Logout
    path("Logout", auth_views.LogoutView.as_view(next_page="login"), name="Logout"),

#passwordchange
    path("passwordchange/", auth_views.PasswordChangeView.as_view(template_name="app/passwordchange.html", form_class=Mypasswordchangeform, success_url="/passwordchangedone/"), name="passwordchange"),
#passwordchangedone
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"), name="passwordchange"),
#password_reset
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="app/password_reset.html", form_class=MypasswordResetform), name="password-reset"),
#password_reset_done
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), name="password_reset_done"),
#password_reset_confirm
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html", form_class=Mysetpasswordform), name="password_reset_confirm"),
#password_reset_complete
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), name="password_reset_complete"),

#registration
    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='payment'),
    path('orders/', views.orders, name='orders'),

    path("search/", views.search, name="search"),
  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
