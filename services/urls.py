from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('', home_page, name="home-page"),
    path('service/<int:id>/', service_page, name="service-page"),
    path('service/create/', create_service_page, name="create-service"),
    path('create-service-form/', service_create_form, name="create-service-form"),
    path('service/update/<int:id>/', update_service_page, name="update-service"),
    path('update-service-form/<int:id>/', service_update_form, name="update-service-form"),
    path('service/delete/<int:id>/', service_delete, name="delete-service"),
    path('checkout/<int:id>/', checkout_page, name="checkout-page"),
    path('thank-you/', thank_you_page, name="thank-you-page"),
    path('subscriptions/', subscription_page, name="subscription-page"),
]

router.register(r'api/services', ServiceViewSet)
urlpatterns += router.urls
# List Services: GET /api/services/
# Create Services: POST /api/services/
# Retrieve Services: GET /api/services/{pk}/
# Update Services: PUT /api/services/{pk}/ or PATCH /api/services/{pk}/
# Delete Services: DELETE /api/services/{pk}/
