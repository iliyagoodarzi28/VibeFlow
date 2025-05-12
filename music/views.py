from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from .models import (
    Song, Album, Artist, Genre, Playlist,
    ArtistCollaboration,
    SongLike, SongComment, SongView
)
from .forms import CommentForm
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# ------------------------  song list view ------------------------
class SongListView(ListView):
    model = Song
    template_name = 'music/song_list.html'
    context_object_name = 'songs'
    paginate_by = 6

# ------------------------  song detail view ------------------------
class SongDetailView(View):
    def get(self, request, *args, **kwargs):
        song = get_object_or_404(Song, pk=kwargs.get('pk'))
        form = CommentForm()
        comments = song.comments.all()
        # Views are incremented via AJAX, not here
        return render(request, 'music/song_detail.html', {
            'song': song,
            'form': form,
            'comments': comments,
        })

    def post(self, request, *args, **kwargs):
        song = get_object_or_404(Song, pk=kwargs.get('pk'))
        form = CommentForm(request.POST)
        user = request.user if request.user.is_authenticated else None
        if form.is_valid():
            comment = form.save(commit=False)
            comment.song = song
            if user:
                comment.user = user
            comment.save()
            return redirect('music:song_detail', pk=song.pk)
        comments = song.comments.all()
        return render(request, 'music/song_detail.html', {
            'song': song,
            'form': form,
            'comments': comments,
        })

# ------------------------  song play (AJAX view increment) ------------------------
class SongPlayView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        song = get_object_or_404(Song, pk=kwargs.get('pk'))
        user = request.user if request.user.is_authenticated else None
        SongView.objects.create(song=song, user=user)
        return JsonResponse({'success': True, 'views_count': song.views.count()})

# ------------------------  random song view ------------------------
class RandomSongView(View):
    def get(self, request, *args, **kwargs):
        songs = list(Song.objects.all())
        if songs:
            random_song = random.choice(songs)
            song_url = reverse('music:song_detail', args=[random_song.pk])
            return JsonResponse({'song_url': song_url})
        return JsonResponse({'song_url': ''})

# ------------------------  comment delete view ------------------------
class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(SongComment, pk=pk)
        if comment.user == request.user:
            comment.delete()
        return redirect('music:song_detail', pk=comment.song.pk)

# ------------------------  comment update view ------------------------
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = SongComment
    form_class = CommentForm
    template_name = 'music/edit_comment.html'
    login_url = 'login'

    def get_queryset(self):
        return SongComment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('music:song_detail', kwargs={'pk': self.object.song.pk})

# ------------------------  song like view ------------------------
class SongLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        like, created = SongLike.objects.get_or_create(song=song, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'liked': liked, 'likes_count': song.likes.count()})
        return redirect('music:song_detail', pk=pk)

# ------------------------  album list view ------------------------
class AlbumListView(ListView):
    model = Album
    template_name = 'music/album_list.html'
    context_object_name = 'albums'
    paginate_by = 10

# ------------------------  album detail view ------------------------
class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_detail.html'
    context_object_name = 'album'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.object
        context['songs'] = album.songs.all()
        return context

# ------------------------  artist list view ------------------------
class ArtistListView(ListView):
    model = Artist
    template_name = 'music/artist_list.html'
    context_object_name = 'artists'
    paginate_by = 12

# ------------------------  artist detail view ------------------------
class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'music/artist_detail.html'
    context_object_name = 'artist'
    paginate_by = 5

# ------------------------  follow artist view ------------------------
class FollowArtistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        artist.followers.add(request.user)
        return redirect('music:artist_detail', pk=pk)

# ------------------------  unfollow artist view ------------------------
class UnfollowArtistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        artist = get_object_or_404(Artist, pk=pk)
        artist.followers.remove(request.user)
        return redirect('music:artist_detail', pk=pk)  


# ------------------------  genre list view ------------------------
class GenreListView(ListView):
    model = Genre
    template_name = 'music/genre_list.html'
    context_object_name = 'genres'
    paginate_by = 10

# ------------------------  genre detail view ------------------------
class GenreDetailView(DetailView):
    model = Genre
    template_name = 'music/genre_detail.html'
    context_object_name = 'genre'
    paginate_by = 3



# ------------------------  playlist list view ------------------------
class PlaylistListView(ListView):
    model = Playlist
    template_name = 'music/playlist_list.html'
    context_object_name = 'playlists'
    paginate_by = 10

# ------------------------  playlist detail view ------------------------
class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'music/playlist_detail.html'
    context_object_name = 'playlist'

# ------------------------  playlist create view ------------------------
class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['title', 'description', 'is_public']
    template_name = 'music/playlist_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('music:playlist_detail', kwargs={'pk': self.object.pk})

# ------------------------  playlist add song view ------------------------
class PlaylistAddSongView(LoginRequiredMixin, View):
    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
        song_id = request.POST.get('song_id')
        song = get_object_or_404(Song, pk=song_id)
        playlist.songs.add(song)
        return redirect('music:playlist_detail', pk=pk)


# ------------------------  artist collaboration detail view ------------------------
class ArtistCollaborationDetailView(DetailView):
    model = ArtistCollaboration
    template_name = 'music/collaboration_detail.html'
    context_object_name = 'collaboration'






from django.views.generic import View
from django.db.models import Q
from django.shortcuts import render
from .models import Artist, Album, Song, Genre

class SearchView(View):
    template_name = "music/search_results.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        results = {
            'artists': [],
            'albums': [],
            'songs': [],
            'genres': [],
        }

        if query:
            results['artists'] = Artist.objects.filter(
                Q(name__icontains=query) | Q(bio__icontains=query)
            ).distinct()

            results['albums'] = Album.objects.filter(
                Q(title__icontains=query)
            ).distinct()

            results['songs'] = Song.objects.filter(
                Q(title__icontains=query) | Q(text__icontains=query)
            ).distinct()

            results['genres'] = Genre.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).distinct()

        context = {
            'query': query,
            'results': results,
        }
        return render(request, self.template_name, context)
