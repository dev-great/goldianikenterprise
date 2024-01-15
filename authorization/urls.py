from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


app_name = 'authorization'

urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('registration/', registration_view, name='registration_view'),
    path('logout/', logout_view, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('core:index')), name='logout'),
    path('changePassword/', changePassword, name='changePassword'),
]
