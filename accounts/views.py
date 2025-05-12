from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.views.generic import TemplateView
from django.views import View

class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration was successful!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please fix the existing errors!")
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('main:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, "Welcome!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "The username or password is incorrect.")
        return super().form_invalid(form)



class LogoutView(TemplateView):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have successfully logged out of your account.")
        return self.render_to_response(self.get_context_data())


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

class FollowedArtistsView(ListView):
    template_name = 'accounts/followed_artists.html'
    context_object_name = 'followed_artists'
    paginate_by = 6

    def get_queryset(self):
        User = get_user_model()
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        # Assuming a ManyToManyField named 'followed_artists' on the User model
        return user.following.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['profile_user'] = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return context



class LikedSongsView(ListView):
    template_name = 'accounts/liked_songs.html'
    context_object_name = 'liked_songs'
    paginate_by = 10

    def get_queryset(self):
        User = get_user_model()
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        # Assuming a ManyToManyField named 'liked_songs' on the User model
        return user.song_likes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['profile_user'] = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return context

