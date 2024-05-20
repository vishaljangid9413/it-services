from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()


urlpatterns = [
    path('register/', register_page, name='user-register'),
    path('user-register-form/', registeration_form, name='user-register-form'),
    path('login/', login_page, name='user-login'),
    path('user-login-form/', login_form, name='user-login-form'),
    path('logout/', logout, name='user-logout'),

    # ** APIs **
    path("api/getOTP/", GetOTP.as_view(), name='get-otp'),
    path('api/register/', UserRegistration.as_view(), name='registration-api'),
    path('api/login/', LoginView.as_view(), name='login-api'),
    path('api/logout/', LogoutView.as_view(), name='logout-api'),
    path('api/forgetPassword/', ForgetPasswordView.as_view(), name='forget-password-api'),    
]

router.register(r'api/users', UserViewSet, basename='user')
urlpatterns += router.urls
# List Users: GET /api/users/
# Create User: POST /api/users/
# Retrieve User: GET /api/users/{pk}/
# Update User: PUT /api/users/{pk}/ or PATCH /api/users/{pk}/
# Delete User: DELETE /api/users/{pk}/
