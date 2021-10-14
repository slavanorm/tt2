from image_handler import views

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views


router = routers.SimpleRouter()
router.register("images", views.ImageViewSet,basename='img')

urlpatterns = [
    path("", include(router.urls)),
    path(
        "images/<int:width>x<int:height>/<str:filename>",
        views.ImageViewSet.resized,
        name='img_resized'
    ),  # not the best but fastest
    path(
        "api/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
