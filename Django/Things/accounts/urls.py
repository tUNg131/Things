from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    # path('signup/', SignUpUser.as_view(), name='signup')
]
