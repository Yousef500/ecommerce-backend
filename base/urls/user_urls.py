from django.urls import path

from base.views.user_views import MyTokenObtainPairView, UserProfileAPIView, \
    UserListAPIView, UserCreateAPIView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('profile/', UserProfileAPIView.as_view(), name="user-profile"),
    path('register/', UserCreateAPIView.as_view(), name="user-create"),
    path('', UserListAPIView.as_view(), name="user-list"),

]
