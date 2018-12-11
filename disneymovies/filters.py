import django_filters
from disneymovies.models import Movie, Genre, Director


class DisneyMovieFilter(django_filters.FilterSet):
	movie_title = django_filters.CharFilter(
		field_name='movie_title',
		label='Movie Title',
		lookup_expr='icontains'
	)

	#filter by genre
	genre_name = django_filters.ModelChoiceFilter(
		field_name='genre__genre_name',
		label='Genre',
		queryset = Genre.objects.all().order_by('genre_name'),
		lookup_expr='exact'
	)

	#filter by director
	director_name = django_filters.ModelChoiceFilter(
		field_name='director__director_name',
		label='Director',
		queryset = Director.objects.all().order_by('director_name'),
		lookup_expr='exact'
	)

	#filter by song
	song = django_filters.CharFilter(
		field_name='song',
		label='Song',
		lookup_expr='icontains'
	)


	class Meta:
		model = Movie
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []