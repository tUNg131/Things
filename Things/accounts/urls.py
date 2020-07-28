from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),

    path('password/change/', views.PasswordChangeUser.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDoneUser.as_view(), name='password_change_done'),

    path('password/reset/', views.PasswordResetUser.as_view(), name='password_reset'),
    path('password/reset/done/', views.PasswordResetDoneUser.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>', views.PasswordResetConfirmUser.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompletleUser.as_view(), name='password_reset_complete'),
    
    path('<int:pk>/settings/', views.Settings.as_view(), name='settings')
]
