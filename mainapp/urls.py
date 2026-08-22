from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('delete_food_admin/<int:id>/', views.delete_food_admin, name='delete_food_admin'),
    # Feedback
    path('add_feedback/<int:restaurant_id>/', views.add_feedback, name='add_feedback'),
    path('view_feedback_restaurant/', views.view_feedback_restaurant, name='view_feedback_restaurant'),
    path('view_feedback_admin/', views.view_feedback_admin, name='view_feedback_admin'),

    # Admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('delete_restaurant/<int:id>/', views.delete_restaurant, name='delete_restaurant'),
    path('view_orders_admin/', views.view_orders_admin, name='view_orders_admin'),

    # Restaurant
    path('restaurant_register/', views.restaurant_register, name='restaurant_register'),
    path('restaurant_dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_food/', views.add_food, name='add_food'),
    path('delete_food/<int:id>/', views.delete_food, name='delete_food'),
    path('view_orders_restaurant/', views.view_orders_restaurant, name='view_orders_restaurant'),
    path('update_order_status/<int:id>/', views.update_order_status, name='update_order_status'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),


    # User
    path('browse_restaurants/', views.browse_restaurants, name='browse_restaurants'),
    path('view_menu/<int:id>/', views.view_menu, name='view_menu'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),

]