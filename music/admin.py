from django.contrib import admin
from .models import Song, Album, Artist, Genre, Playlist, ArtistCollaboration, SongLike, SongComment, SongView

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'release_date')
    search_fields = ('title', 'artist__name', 'album__title')
    list_filter = ('release_date', 'artist', 'album', 'genres')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist__name')
    list_filter = ('release_date', 'artist')

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public')
    search_fields = ('title', 'user__username')
    list_filter = ('is_public',)

@admin.register(ArtistCollaboration)
class ArtistCollaborationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'release_date')
    search_fields = ('id',)
    list_filter = ('release_date',)



@admin.register(SongLike)
class SongLikeAdmin(admin.ModelAdmin):
    list_display = ('song', 'user', 'timestamp')
    search_fields = ('song__title', 'user__username')
    list_filter = ('timestamp',)

@admin.register(SongComment)
class SongCommentAdmin(admin.ModelAdmin):
    list_display = ('song', 'user', 'timestamp')
    search_fields = ('song__title', 'user__username', 'text')
    list_filter = ('timestamp',)

@admin.register(SongView)
class SongViewAdmin(admin.ModelAdmin):
    list_display = ('song', 'user', 'timestamp')
    search_fields = ('song__title', 'user__username')
    list_filter = ('timestamp',)
