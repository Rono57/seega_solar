"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login,name='login'),
      path('adm',views.adm),
      path('staff',views.staff),
      path('user',views.user),
    path('reply/<id>',views.reply),
    path('manage_staff',views.manage_staff, name='manage_staff'),
    path('manage_vendor',views.manage_vendor, name='manage_vendor'),
    path('manage_package',views.manage_package, name='manage_package'),
    path('manage_item',views.manage_item, name='manage_item'),
    
    path('user_reg',views.user_reg, name='user_reg'),
    
    
    
    path('adm_com',views.adm_com),
    
    path('adm_order',views.adm_order),
    
    
    path('send_estimate/<id>',views.send_estimate),
    
    path('make_payment/<id>',views.make_payment),
    
    path('reject/<id>',views.reject_order),
    path('approve_order/<id>',views.approve_order),
    path('up_com/<id>',views.up_com),
    path('remove/<id>',views.remove),
    path('book_ser/<id>',views.book_ser),
    
    path('assign_sbook/<id>',views.assign_sbook),
    
    
    path('manage_services',views.manage_services, name='manage_services'),
    path('user_view_ser',views.user_view_ser, name='user_view_ser'),
    path('user_view_sbook',views.user_view_sbook, name='user_view_sbook'),
    path('user_view_assigned_sbook/<id>',views.user_view_assigned_sbook, name='user_view_assigned_sbook'),
    
    
    
    
    path('sbooking',views.sbooking, name='sbooking'),
    
    
    
    
    
    
    path('assign_worker/<id>',views.assign_worker),
    
    
    path('adm_review',views.admin_review),
    
    path('stf_task',views.stf_task),
    
    path('st_used/<id>',views.st_used,name='st_used'),
    
    path('st_pack/<id>',views.st_pack,name='st_pack'),
    
    path('chat_with_admin',views.chat_with_admin,name='chat_with_admin'),
    
      path("chat_with_staff/<int:id>/", views.chat_with_staff, name="chat_with_staff"),
    path("send_message_staff/", views.send_message_staff, name="send_message_staff"),
    path('send_message/', views.send_message, name='send_message'),
    
  
    
    
    
    
    
    
    
    
    
    
    
    path('user_package',views.user_package),
    
    path('send_request/<id>',views.send_request),
    
    
    path('user_complaint',views.user_complaint),
    
    path('user_reviews',views.user_reviews),
    
    path('user_order',views.user_order),
    
    
    
    
    
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    
     path('edit_package/<int:package_id>/', views.edit_package, name='edit_package'),
    path('delete_package/<int:package_id>/', views.delete_package, name='delete_package'),
    
    
    
   path('user_profile/', views.user_profile, name='user_profile'),
path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),



      
      
      
      
    
    
]
