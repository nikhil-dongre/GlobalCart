"""globalcart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # path('admin/', include(('admin_honeypot.urls', 'admin_honeypot'), namespace='admin_honeypot')),

    # If you want to change for the url of admin forr security purposes. like 
    # path('secureloginglobalcart/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('',views.home ,name='home'),
    path('store/',include('store.urls') ),
    path('cart/',include('carts.urls') ),
    path('accounts/',include('accounts.urls') ),

    # order path url 
    path('orders/',include('orders.urls') )


] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
