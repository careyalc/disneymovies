from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import DisneyMovie
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
	model = DisneyMovie
	context_object_name = 'movies'
	template_name = 'disneymovies/home.html'

	def get_queryset(self):
		return DisneyMovie.objects.all().order_by('movie_title')

class MovieDetailView(generic.DetailView):
	model = DisneyMovie
	context_object_name = 'movie'
	template_name = 'disneymovies/movie_detail.html'