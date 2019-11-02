from django.urls import path
from .views import (
	signout,
)

urlpatterns = [
    path('signout/', signout, name="signout"),
]