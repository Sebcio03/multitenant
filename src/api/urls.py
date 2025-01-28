from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("users/", include("api.users.urls")),
    path("tenants/", include("api.tenants.urls")),
    path("organizations/", include("api.organizations.urls")),
    path("departments/", include("api.departments.urls")),
    path("customers/", include("api.customers.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
