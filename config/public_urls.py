from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/restaurants/', include("apps.restaurants.urls")),

    # ↓ tell spectacular to scan THIS file
    path('api/schema/', SpectacularAPIView.as_view(urlconf='config.public_urls'), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]