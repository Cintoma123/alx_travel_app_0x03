"""
URL configuration for alx_travel_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework import serializers
from listings.models import Listing, Booking
from listings.views import ListingViewSet ,BookingViewSet 
from rest_framework import status
from listings.serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
#from drf_spectacular.views import (
    #SpectacularAPIView,
    #SpectacularSwaggerView,
   # SpectacularRedocView,
#)from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API documentation using Swagger UI",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="calistusumehnnachebe@email.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



router = DefaultRouter()
router.register(r'listing', ListingViewSet)
#router.register(r'user', UserViewSet)
router.register(r'booking', BookingViewSet)
    

urlpatterns = [
      # OpenAPI schema
    #path('admin/', admin.site.urls),
    # Swagger UI
   # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc UI (optional)
    #re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('retrieve_bookings_made_by_user/', ListingViewSet.retrieve_bookings_made_by_user, name='retrieve_bookings_made_by_user'),
    path('list_made_by_user/', ListingViewSet.list_made_by_user, name='list_made_by_user'),
    path('delete_bookings_made_by_user/', ListingViewSet.delete_bookings_made_by_user, name='delete_bookings_made_by_user'),
    path('email_message_post/', BookingViewSet.email_message_post, name='email_message_post'),
    path('updated_bookings_made_by_user/', ListingViewSet.updated_bookings_made_by_user, name='updated_bookings_made_by_user'),
    path('', include(router.urls)),

]

