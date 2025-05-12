from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('followed-artists/<int:pk>/', views.FollowedArtistsView.as_view(), name='followed_artists'),
    path('liked-songs/<int:pk>/', views.LikedSongsView.as_view(), name='liked_songs'),

]
