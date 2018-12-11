from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Movie, MovieCharacter, Credit
# from .forms import HeritageSiteForm
from .filters import DisneyMovieFilter
import django_filters
from django_filters.views import FilterView

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

class AboutPageView(generic.TemplateView):
	template_name = 'disneymovies/about.html'

class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'movie'
	template_name = 'disneymovies/movie_detail.html'

	def get_queryset(self):
		return Movie.objects.all().select_related('genre', 'director').order_by('movie_title')


@method_decorator(login_required, name='dispatch')
class CharPageView(generic.ListView):
	model = MovieCharacter
	context_object_name = 'movie_characters'
	template_name = 'disneymovies/movie_char.html'
	# paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return MovieCharacter.objects.all().order_by('movie_character_name')


@method_decorator(login_required, name='dispatch')
class CharDetailView(generic.DetailView):
	model = MovieCharacter
	context_object_name = 'movie_character'
	template_name = 'disneymovies/char_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	# def get_queryset(self):
	# 	return .objects.select_related('credit', 'actor').order_by('movie_character_name')

	# def get_queryset(self):
	# 	return Credit.objects.all().select_related('actor', 'movie_character').order_by('movie_character_name')


class MovieFilterView(FilterView):
	filterset_class = DisneyMovieFilter
	template_name = 'disneymovies/movie_filter.html'


#############
# class PaginatedFilterView(generic.View):
# 	"""
# 	Creates a view mixin, which separates out default 'page' keyword and returns the
# 	remaining querystring as a new template context variable.
# 	https://stackoverflow.com/questions/51389848/how-can-i-use-pagination-with-django-filter
# 	"""
# 	def get_context_data(self, **kwargs):
# 		context = super(PaginatedFilterView, self).get_context_data(**kwargs)
# 		if self.request.GET:
# 			querystring = self.request.GET.copy()
# 			if self.request.GET.get('page'):
# 				del querystring['page']
# 			context['querystring'] = querystring.urlencode()
# 		return context
