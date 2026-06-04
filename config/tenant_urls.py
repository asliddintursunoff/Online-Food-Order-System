from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("apps.products.api.urls")),
    path('api/orders/', include("apps.orders.api.urls")),
    path('api/', include("apps.users.api.urls")),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ↓ tell spectacular to scan THIS file
    path('api/schema/', SpectacularAPIView.as_view(urlconf='config.tenant_urls'), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)