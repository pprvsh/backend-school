
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from admissions.views import AdmissionInquiryViewSet
from faculty.views import FacultyViewSet
from notices.views import NoticeViewSet


router = DefaultRouter()

router.register(
    r"notices",
    NoticeViewSet,
    basename="notice",
)

router.register(
    r"faculty",
    FacultyViewSet,
    basename="faculty",
)

router.register(
    r"admissions",
    AdmissionInquiryViewSet,
    basename="admission",
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT authentication endpoints
    path(
        "api/v1/auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Existing API endpoints
    path("api/", include(router.urls)),
]
