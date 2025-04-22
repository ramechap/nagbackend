from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('verify-otp', views.verify_otp, name='verify_otp'),
    path('signin', views.signup, name='signup'),
    path('login', views.loginn, name='login'),  # Changed from 'loginn' to 'login'
    path('logout', views.logout_view, name='logout'),
    path('create-profile', views.create_profile, name='create_profile'),
    path('profile', views.view_profile, name='view_profile'),
    path('check-auth', views.check_auth, name='check_auth'),
   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
