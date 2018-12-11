from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Movie, MovieCharacter, Credit
# from .forms import HeritageSiteForm
# from .filters import HeritageSiteFilter
# import django_filters
# from django_filters.views import FilterView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse, reverse_lazy, resolve

# from django import forms
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit


def index(request):
	return HttpResponse("Hello, world!!!")


class HomePageView(generic.ListView):
	model = Movie
	context_object_name = 'movies'
	template_name = 'disneymovies/home.html'

	# def get_queryset(self):
	# 	return Movie.objects.all().select_related('director').order_by('movie_title')

class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'movie'
	template_name = 'disneymovies/movie_detail.html'

	def get_queryset(self):
		return Movie.objects.all().select_related('genre', 'director').order_by('movie_title')


class CharPageView(generic.ListView):
	model = MovieCharacter
	context_object_name = 'movie_characters'
	template_name = 'disneymovies/movie_char.html'

	def get_queryset(self):
		return MovieCharacter.objects.all().order_by('movie_character_name')


class CharDetailView(generic.DetailView):
	model = MovieCharacter
	context_object_name = 'movie_character'
	template_name = 'disneymovies/char_detail.html'

	# def get_queryset(self):
	# 	return MovieCharacter.objects.all().select_related('credit', 'actor').order_by('movie_character_name')

	# def get_queryset(self):
	# 	return Credit.objects.all().select_related('actor', 'movie_character').order_by('movie_character_name')

