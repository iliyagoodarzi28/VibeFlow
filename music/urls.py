from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
    # Song URLs
    path('', views.SongListView.as_view(), name='song_list'),
    path('<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    path('<int:pk>/like/', views.SongLikeView.as_view(), name='song_like'),
            # Album URLs
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),

    # Artist URLs
    path('artists/', views.ArtistListView.as_view(), name='artist_list'),
    path('artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),

    # Genre URLs
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),

    # Playlist URLs
    path('playlists/', views.PlaylistListView.as_view(), name='playlist_list'),
    path('playlists/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlists/create/', views.PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlists/<int:pk>/add_song/', views.PlaylistAddSongView.as_view(), name='playlist_add_song'),

    # Artist Collaboration URLs
    path('collaborations/<int:pk>/', views.ArtistCollaborationDetailView.as_view(), name='collaboration_detail'),

    

    # Comment URLs
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),


    path('random-song/', views.RandomSongView.as_view(), name='random_song'),
    path('<int:pk>/play/', views.SongPlayView.as_view(), name='song_play'),


    # Follow/Unfollow Artist .URLs
    path('artists/<int:pk>/follow/', views.FollowArtistView.as_view(), name='follow_artist'),
    path('artists/<int:pk>/unfollow/', views.UnfollowArtistView.as_view(), name='unfollow_artist'),



    # Search URL
    path('search/', views.SearchView.as_view(), name='search'),
]