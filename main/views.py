from django.views.generic import TemplateView
from music.models import Song, Album, Artist
from site_info.models import SiteInfo

import random
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        user = request.user

        # Get site info (assume singleton)
        try:
            site_info = SiteInfo.objects.first()
        except Exception:
            site_info = None

        # Latest 6 songs (by release_date desc, fallback to pk desc)
        latest_songs = Song.objects.order_by('-release_date', '-pk')[:6]

        # Latest 6 albums (by release_date desc, fallback to pk desc)
        latest_albums = Album.objects.order_by('-release_date', '-pk')[:6]

        # Featured artists: show up to 6 verified, fallback to most recent if not enough
        featured_artists = list(Artist.objects.filter(is_verified=True).order_by('-debut_date', '-pk')[:6])
        if len(featured_artists) < 6:
            needed = 6 - len(featured_artists)
            extra_artists = Artist.objects.exclude(pk__in=[a.pk for a in featured_artists]).order_by('-debut_date', '-pk')[:needed]
            featured_artists += list(extra_artists)

        # Artists followed by the user (if authenticated)
        followed_artists = []
        if user.is_authenticated:
            followed_artists = Artist.objects.filter(followers=user).order_by('name')[:6]

        # Songs liked by the user (if authenticated)
        liked_songs = []
        if user.is_authenticated and hasattr(user, 'songlike_set'):
            liked_songs = Song.objects.filter(songlike__user=user).order_by('-songlike__timestamp')[:6]

        # Recently played songs (if authenticated and ListeningHistory model exists)
        recently_played = []
        try:
            from music.models import ListeningHistory
            if user.is_authenticated:
                recently_played = (
                    Song.objects.filter(listeninghistory__user=user)
                    .order_by('-listeninghistory__timestamp')
                    .distinct()[:6]
                )
        except ImportError:
            recently_played = []

        # Random song suggestions (6 random songs)
        song_count = Song.objects.count()
        random_songs = []
        if song_count > 0:
            random_ids = random.sample(list(Song.objects.values_list('pk', flat=True)), min(6, song_count))
            random_songs = list(Song.objects.filter(pk__in=random_ids))

        # Songs with the most views (top 6)
        # Use annotation to count related SongView objects
        most_viewed_songs = (
            Song.objects.annotate(num_views=Count('views'))
            .order_by('-num_views', '-pk')[:6]
        )
        # For template compatibility, attach the view count as 'views' attribute
        for song in most_viewed_songs:
            song.views_count = song.num_views

        context.update({
            'site_info': site_info,
            'latest_songs': latest_songs,
            'latest_albums': latest_albums,
            'featured_artists': featured_artists,
            'followed_artists': followed_artists,
            'liked_songs': liked_songs,
            'recently_played': recently_played,
            'random_songs': random_songs,
            'most_viewed_songs': most_viewed_songs,
        })
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'




