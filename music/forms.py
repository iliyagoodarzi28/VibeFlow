from django import forms
from .models import Playlist, SongComment

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description', 'songs']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'songs': forms.SelectMultiple(attrs={'size': 10}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = SongComment
        fields = ['name','text']
        labels = {
            'name': 'Name',
            'text': 'Comment',
        }



