from django.urls import path,include
from . import views

urlpatterns = [
    path('place_orders/',views.place_order ,name='place_order'), # type: ignore
    path('payments/',views.payments ,name='payments'), # type: ignore

]
