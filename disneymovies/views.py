from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Movie, MovieCharacter, Credit
from .forms import MovieForm
from .filters import DisneyMovieFilter
import django_filters
from django_filters.views import FilterView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse, reverse_lazy, resolve

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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

@method_decorator(login_required, name='dispatch')
class MovieCreateView(generic.View):
	model = Movie
	form_class = MovieForm
	success_message = "Disney Movie added successfully"
	template_name = 'disneymovies/movie_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = MovieForm(request.POST)
		if form.is_valid():
			movie = form.save(commit=False)
			movie.save()
			for movie_character in form.cleaned_data['movie_character']:
				Credit.objects.create(movie=movie, movie_character=movie_character)
				#def not sure if this is right
			return redirect(movie) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'disneymovies/movie_new.html', {'form': form})

	def get(self, request):
		form = MovieForm()
		return render(request, 'disneymovies/movie_new.html', {'form': form})




@method_decorator(login_required, name='dispatch')
class MovieUpdateView(generic.UpdateView):
	model = Movie
	form_class = MovieForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'movie'
	# pk_url_kwarg = 'site_pk'
	success_message = "Disney Movie updated successfully"
	template_name = 'disneymovies/movie_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		movie = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		movie.save()

		# Current country_area_id values linked to site
		old_ids = Credit.objects\
			.values_list('movie_character_id', flat=True)\
			.filter(movie_id=movie.movie_id)

		# New countries list
		new_movie_characters = form.cleaned_data['movie_character']

		# TODO can these loops be refactored?

		# New ids
		new_ids = []

		# Insert new unmatched character entries
		for movie_character in new_movie_characters:
			new_id = movie_character.movie_character_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				Credit.objects \
					.create(movie=movie, movie_character=movie_character)

		# Delete old unmatched character entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				Credit.objects \
					.filter(movie_id=movie.movie_id, movie_character_id=old_id) \
					.delete()

		return HttpResponseRedirect(movie.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)


@method_decorator(login_required, name='dispatch')
class MovieDeleteView(generic.DeleteView):
	model = Movie
	success_message = "Disney Movie deleted successfully"
	success_url = reverse_lazy('movie')
	context_object_name = 'movie'
	template_name = 'disneymovies/movie_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		Credit.objects \
			.filter(heritage_site_id=self.object.movie_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())