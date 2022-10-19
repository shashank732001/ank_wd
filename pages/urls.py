
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.homepage,name='home' ),
    path('products/',views.productpage,name='products' ),
    path('status/',views.statuspage,name='status' ),
    path('cart/',views.cart,name='cart' ),
    path('checkout/',views.checkout,name='checkout' ),
    path('dashboard/',views.dashboardpage,name='dashboard' ),


##login and authentication
    path('login/',views.login,name='login' ),
    path('logout/',views.logout,name='logout' ),
    path('register/',views.register,name='register' ),


    path('update_item/',views.updateItem,name='update_item' ),
    path('update_status/<str:pk>/',views.cartitemUpdate,name='update-status' ),
    path('delete_item/<str:pk>/',views.cartitemDelete,name='delete-cart-item' ),


    path('add_product/',views.addProduct,name='add-product' ),
    path('edit_product/<str:pk>/',views.editProduct,name='edit-product' ),
    path('view_product/<str:pk>/',views.viewProduct,name='view-product' ),


   ##reset password functionality 

   path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="pages/password_reset.html"),name='password_reset'),

   path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="pages/password_reset_sent.html"),name='password_reset_done'),

   path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="pages/password_reset_form.html"),name='password_reset_confirm'),

   path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="pages/password_reset_done.html"),name='password_reset_complete'),

]
