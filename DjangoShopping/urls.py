"""DjangoShopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from mycontroller import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',indexpage),
    path('addcategorypage',addcategorypage),
    path('addcategoryaction',addcategoryaction),
    path('viewcategorypage',viewcategorypage),
    path('viewcategoryaction',viewcategoryaction),
    path('deletecategoryaction',deletecategoryaction),
    path('usersignuppage',usersignuppage),
    path('usersignupaction',usersignupaction),
    path('addproductpage',addproductpage),
    path('addproductaction',addproductaction),
    path('viewproductpage',viewproductpage),
    path('viewproductaction',viewproductaction),
    path('deleteproductaction',deleteproductaction),
    path('showallproductpage',showallproductpage),
    path('showallproductaction',showallproductaction),
    path('addtocartaction',addtocartaction),
    path('mycart',mycart),
    path('mycartaction',mycartaction),
    path('deletefromcart',deletefromcart),
    path('proceedtopay',proceedtopay),
    path('userlogin',userlogin),
    path('userloginaction',userloginaction),
    path('userlogout',userlogout),
    path('userhomepage',userhomepage),
    path('billinginfo',billinginfo),
    path('checkoutaction',checkoutaction),
    path('thankspage',thankspage),
    path('pendingorderpage',pendingorderpage),
    path('pendingordersaction',pendingordersaction),
    path('approve_reject_action',approve_reject_action),
    path('myorders',myorders),
    path('myordersaction',myordersaction),
    path('showproductbycategorypage',showproductbycategorypage),
    path('viewproductbycategory',viewproductbycategory),

]
