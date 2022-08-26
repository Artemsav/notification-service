"""testfeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from mailing.views import ClientViewSet, MailingViewSet, MessageViewSet
from rest_framework import permissions, routers
from mailing.views import redirect2admin
import testfeed.settings as settings

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailings', MailingViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Messages API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="studentbedn@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

swgurlpatterns = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect2admin),
    path('api/', include(router.urls)),
    path('api-auth/', include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += swgurlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
