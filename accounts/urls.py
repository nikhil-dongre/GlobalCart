from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logut/',views.logout,name='logut'),
    # path('activate/<uidb64>/token/', views.activate, name='activate')
    path('activate/<uidb64>/<token>/', views.activate, name='activate')

]
