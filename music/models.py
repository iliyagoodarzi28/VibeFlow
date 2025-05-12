from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Genre Name")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

class BaseMusicEntity(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    release_date = models.DateField(blank=True, null=True, verbose_name="Release Date")

    class Meta:
        abstract = True
        verbose_name = "Music Entity"
        verbose_name_plural = "Music Entities"
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_date']),
        ]

class Artist(models.Model):
    name = models.CharField(max_length=200, verbose_name="Artist Name")
    bio = models.TextField(blank=True, verbose_name="Biography")
    image = models.ImageField(upload_to='artists/', blank=True, null=True, verbose_name="Artist Image")
    debut_date = models.DateField(blank=True, null=True, verbose_name="Debut Date")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Genre")
    followers = models.ManyToManyField(User, related_name='following', blank=True, verbose_name="Followers")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Artist"
        verbose_name_plural = "Artists"

class Album(BaseMusicEntity):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums', verbose_name="Artist")
    cover = models.ImageField(upload_to='albums/', blank=True, null=True, verbose_name="Album Cover")
    genres = models.ManyToManyField(Genre, related_name='albums', blank=True, verbose_name="Genres")
    rating = models.FloatField(blank=True, null=True, verbose_name="Album Rating")

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

    class Meta(BaseMusicEntity.Meta):
        verbose_name = "Album"
        verbose_name_plural = "Albums"

class Song(BaseMusicEntity):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs', verbose_name="Artist")
    album = models.ForeignKey('Album', on_delete=models.SET_NULL, related_name='songs', null=True, blank=True, verbose_name="Album")
    genres = models.ManyToManyField(Genre, related_name='songs', blank=True, verbose_name="Genres")
    duration = models.DurationField(blank=True, null=True, verbose_name="Duration")
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True, verbose_name="Audio File")
    text = models.TextField(blank=True, help_text="Lyrics or description of the song", verbose_name="Lyrics/Description")
    image = models.ImageField(upload_to='songs/', blank=True, null=True, verbose_name="Song Image")
    rating = models.FloatField(blank=True, null=True, verbose_name="Song Rating")
    collaborations = models.ManyToManyField('ArtistCollaboration', related_name='songs', blank=True, verbose_name="Collaborations")


    @classmethod
    def get_currently_playing(cls):
        """Return the currently playing song, if any."""
        return cls.objects.filter(is_playing=True).first()
    # --- End Song Playing Logic ---

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

    def view_count(self):
        return self.views.count()

    class Meta(BaseMusicEntity.Meta):
        verbose_name = "Song"
        verbose_name_plural = "Songs"

class SongComment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments', verbose_name="Song")
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    text = models.TextField(verbose_name="Comment Text")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Timestamp")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='song_comments', verbose_name="User")

    def __str__(self):
        return f"Comment by {self.name} on {self.song}"

    class Meta:
        verbose_name = "Song Comment"
        verbose_name_plural = "Song Comments"

class SongView(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='views', verbose_name="Song")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='song_views', verbose_name="User")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    def __str__(self):
        return f"View: {self.song.title} by {self.user if self.user else 'Anonymous'}"

    class Meta:
        verbose_name = "Song View"
        verbose_name_plural = "Song Views"

class SongLike(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='likes', verbose_name="Song")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_likes', verbose_name="User")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        unique_together = ('song', 'user')
        verbose_name = "Song Like"
        verbose_name_plural = "Song Likes"

    def __str__(self):
        return f"Like: {self.song.title} by {self.user}"

class Playlist(BaseMusicEntity):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', verbose_name="User")
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True, verbose_name="Songs")
    description = models.TextField(blank=True, verbose_name="Description")
    is_public = models.BooleanField(default=False, verbose_name="Is Public")

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    class Meta(BaseMusicEntity.Meta):
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"

class ArtistCollaboration(models.Model):
    artists = models.ManyToManyField(Artist, related_name='artist_collaborations', verbose_name="Artists")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='artist_collaborations', verbose_name="Song")
    release_date = models.DateField(blank=True, null=True, verbose_name="Release Date")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        artist_names = ", ".join(artist.name for artist in self.artists.all())
        return f"Collaboration on '{self.song.title}' by {artist_names}"

    def display_title(self):
        artist_names = ", ".join(artist.name for artist in self.artists.all())
        return f"{self.song.title} by {artist_names}"
    display_title.short_description = "Title"

    class Meta:
        verbose_name = "Artist Collaboration"
        verbose_name_plural = "Artist Collaborations"

# ListeningHistory model has been cleared as per instruction.
