"""hypercar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from tickets import views
from tickets.views import ProcessingView

urlpatterns = [
    path('menu/', views.menu, name="main-menu"),
    path('get_ticket/change_oil/', views.change_oil, name="change-oil"),
    path('get_ticket/inflate_tires/', views.inflate_tires, name="inflate-tires"),
    path('get_ticket/diagnostic/', views.diagnostic, name="diagnostic"),
    # path('processing/', views.processing_page, name="processing"),
    re_path('processing', ProcessingView.as_view()),
    path('next', views.next_page, name="next-customer")
]

