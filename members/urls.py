from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, PerformanceViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'performances', PerformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('admin/', admin.site.urls),
    #path('api/', include('members.urls')),
    # URLs pour JWT
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]